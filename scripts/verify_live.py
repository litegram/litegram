"""Live verification of Litegram 1.1.0 against the real Telegram API.

Run: BOT_TOKEN=... python -m scripts.verify_live
Covers: chunked multipart upload (buffered + filesystem), URL re-upload,
form-only request, file download. Token is read from the environment and
never written to disk inside the repo.
"""

from __future__ import annotations

import asyncio
import os
import time
from pathlib import Path
from tempfile import gettempdir

from litegram import Bot
from litegram.types import BufferedInputFile, FSInputFile, InputFile, URLInputFile

CHAT_ID = 166775101
PUBLIC_URL = "https://www.python.org/static/img/python-logo.png"


async def verify(bot: Bot) -> None:
    # 1. Chunked multipart upload through the new encoder (bytes in memory).
    start = time.monotonic()
    doc = await bot.send_document(
        chat_id=CHAT_ID,
        document=BufferedInputFile(
            b"litegram 1.1.0 chunked multipart upload verification\n" * 200,
            "litegram-verification.txt",
        ),
        caption="Тест 1/4: chunked multipart, BufferedInputFile",
    )
    assert doc.message_id, "no message id"
    print(f"1. send_document(BufferedInputFile)   OK  {time.monotonic() - start:.2f}s")

    # 2. Chunked multipart upload from the filesystem (aiofiles reader).
    tmp = Path(gettempdir()) / "litegram-verification-fs.png"
    tmp.write_bytes(b"\x89PNG\r\n\x1a\n" + os.urandom(4096))
    start = time.monotonic()
    doc2 = await bot.send_document(
        chat_id=CHAT_ID,
        document=FSInputFile(tmp),
        caption="Тест 2/4: chunked multipart, FSInputFile",
    )
    assert doc2.message_id
    print(f"2. send_document(FSInputFile)         OK  {time.monotonic() - start:.2f}s")
    tmp.unlink()

    # 3. URLInputFile: download a public image and re-upload it as a photo.
    start = time.monotonic()
    photo = await bot.send_photo(
        chat_id=CHAT_ID,
        photo=URLInputFile(PUBLIC_URL),
        caption="Тест 3/4: URLInputFile (download + re-upload)",
    )
    assert photo.photo
    print(f"3. send_photo(URLInputFile)           OK  {time.monotonic() - start:.2f}s")

    # 4. Form-only request (no multipart involved).
    start = time.monotonic()
    msg = await bot.send_message(chat_id=CHAT_ID, text="Тест 4/4: form-only запрос")
    assert msg.message_id
    print(f"4. send_message(form)                 OK  {time.monotonic() - start:.2f}s")

    # 5. File download through the same session.
    destination = Path(gettempdir()) / "litegram-download.txt"
    await bot.download(file=doc.document, destination=destination)
    downloaded = destination.read_bytes()
    assert downloaded.startswith(b"litegram 1.1.0"), "downloaded content mismatch"
    print(f"5. download_file                      OK  ({len(downloaded)} bytes round-trip)")

    await bot.send_message(chat_id=CHAT_ID, text="✅ Все проверки Litegram 1.1.0 пройдены")
    print("ALL PASSED")


def main() -> None:
    token = os.environ.get("BOT_TOKEN")
    if not token:
        msg = "Set BOT_TOKEN"
        raise SystemExit(msg)

    async def run() -> None:
        bot = Bot(token=token)
        try:
            await verify(bot)
        finally:
            await bot.session.close()

    asyncio.run(run())


if __name__ == "__main__":
    main()
