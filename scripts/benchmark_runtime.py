"""Run offline from the repo root: python -m scripts.benchmark_runtime."""

from __future__ import annotations

import argparse
import asyncio
import platform
import sys
from itertools import cycle, islice
from statistics import median
from time import perf_counter_ns
from typing import TYPE_CHECKING, Never

import pydantic

import litegram
from litegram import Bot, Dispatcher, loggers
from litegram.client.session.httpx import HttpxSession

if TYPE_CHECKING:
    from litegram.types import Message

TEXT = "benchmark message"
# Rotate through more IDs than Update.event_type's 128-entry LRU cache holds.
CORPUS_SIZE = 256


class OfflineSession(HttpxSession):
    async def create_client(self) -> Never:
        msg = "The offline benchmark must not create an HTTP client"
        raise RuntimeError(msg)


class Options(argparse.Namespace):
    iterations: int
    repeats: int
    warmup: int


def positive_int(value: str) -> int:
    number = int(value)
    if number < 1:
        msg = "must be a positive integer"
        raise argparse.ArgumentTypeError(msg)
    return number


async def benchmark(options: Options) -> list[int]:
    payloads = cycle(
        {
            "update_id": update_id,
            "message": {
                "message_id": update_id,
                "date": 1_700_000_000,
                "chat": {"id": 42, "type": "private"},
                "from": {"id": 42, "is_bot": False, "first_name": "Benchmark"},
                "text": TEXT,
            },
        }
        for update_id in range(1, CORPUS_SIZE + 1)
    )
    dispatcher = Dispatcher(disable_fsm=True)

    @dispatcher.message()
    async def handle_message(message: Message) -> str | None:
        return message.text

    async with Bot("123456:offline-benchmark", session=OfflineSession()) as bot:

        async def run_batch(count: int) -> int:
            batch = tuple(islice(payloads, count))
            start = perf_counter_ns()
            for payload in batch:
                if await dispatcher.feed_raw_update(bot, payload) != TEXT:
                    msg = "Message handler did not return the expected text"
                    raise RuntimeError(msg)
            return perf_counter_ns() - start

        await run_batch(options.warmup)
        return [await run_batch(options.iterations) for _ in range(options.repeats)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark offline dict-to-Update parsing and sequential message dispatch.")
    parser.add_argument("--iterations", type=positive_int, default=20_000, help="updates per measured repeat (default: 20000)")
    parser.add_argument("--repeats", type=positive_int, default=5, help="number of measured repeats (default: 5)")
    parser.add_argument("--warmup", type=positive_int, default=2_000, help="updates before the first repeat (default: 2000)")
    options = parser.parse_args(namespace=Options())
    loggers.event.disabled = True
    samples = asyncio.run(benchmark(options))
    us_per_update = [sample / (options.iterations * 1_000) for sample in samples]
    median_us = median(us_per_update)
    sys.stdout.write(
        f"{platform.python_implementation()} {platform.python_version()} | {platform.system()} {platform.machine()} | "
        f"litegram {litegram.__version__} | Pydantic {pydantic.__version__}\n"
        f"Litegram source: {litegram.__file__}\n"
        f"feed_raw_update: {options.repeats} x {options.iterations:,} updates; {options.warmup:,} warmup; "
        "one message handler; FSM and event logging disabled\n"
        f"Per-repeat mean (us/update): {', '.join(f'{sample:.2f}' for sample in us_per_update)}\n"
        f"Median: {median_us:.2f} us/update ({1_000_000 / median_us:,.0f} updates/s)\n"
    )


if __name__ == "__main__":
    main()
