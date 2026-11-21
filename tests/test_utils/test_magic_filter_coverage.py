from __future__ import annotations

import operator
import re

import pytest

from litegram import F
from litegram.utils.magic_filter.attrdict import AttrDict
from litegram.utils.magic_filter.exceptions import ParamsConflict, RejectOperations, SwitchModeToAll, SwitchModeToAny
from litegram.utils.magic_filter.helper import resolve_if_needed
from litegram.utils.magic_filter.magic import MagicFilter
from litegram.utils.magic_filter.operations.call import CallOperation
from litegram.utils.magic_filter.operations.cast import CastOperation
from litegram.utils.magic_filter.operations.combination import CombinationOperation, RCombinationOperation
from litegram.utils.magic_filter.operations.extract import ExtractOperation
from litegram.utils.magic_filter.operations.function import FunctionOperation, ImportantFunctionOperation
from litegram.utils.magic_filter.operations.getattr import GetAttributeOperation
from litegram.utils.magic_filter.operations.getitem import EMPTY_SLICE, GetItemOperation
from litegram.utils.magic_filter.operations.selector import SelectorOperation
from litegram.utils.magic_filter.util import and_op, contains_op, in_op, not_contains_op, not_in_op, or_op


def raises(fn):
    try:
        fn()
    except RejectOperations:
        return True
    return False


class Matrix:
    def __matmul__(self, other):
        return "matrix-product"

    def __rmatmul__(self, other):
        return "r-matrix-product"


class TestOperationsDirectly:
    def test_getitem_key_modes_and_rejections(self):
        operation = GetItemOperation("a")
        assert operation.resolve({"a": 42}, {}) == 42
        assert raises(lambda: operation.resolve({"b": 0}, {}))

        with pytest.raises(SwitchModeToAny):
            GetItemOperation(...).resolve([1, 2], {})
        with pytest.raises(SwitchModeToAll) as exc_info:
            GetItemOperation(EMPTY_SLICE).resolve([1, 2], {})
        assert exc_info.value.key == EMPTY_SLICE

    def test_extract_accepts_and_rejects(self):
        operation = ExtractOperation(F.cast(bool))
        assert operation.resolve([True, False], {}) == [True]
        assert operation.resolve(None, {}) is None

    def test_selector_and_call(self):
        assert SelectorOperation(F.cast(bool)).resolve(1, {}) == 1
        assert raises(lambda: SelectorOperation(F.cast(bool)).resolve(0, {}))
        assert CallOperation((2,), {}).resolve(lambda x: x**2, {}) == 4
        assert raises(lambda: CallOperation((), {}).resolve(1, {}))

    def test_cast_and_function_errors(self):
        def fail(_):
            raise RuntimeError("nope")

        assert raises(lambda: CastOperation(fail).resolve(0, {}))
        with pytest.raises(RuntimeError, match="nope"):
            FunctionOperation(fail).resolve(0, {})
        assert raises(lambda: FunctionOperation(int).resolve("not-a-number", {}))

    def test_combinations(self):
        assert CombinationOperation(2, and_op).resolve(True, {}) == 2
        assert RCombinationOperation(2, operator.add).resolve(3, {}) == 5

    def test_helper_resolves_magic(self):
        assert resolve_if_needed(F.cast(int), "4") == 4
        assert resolve_if_needed("plain", "unused") == "plain"

    def test_switch_exception(self):
        assert SwitchModeToAll(EMPTY_SLICE).key == EMPTY_SLICE

    def test_util_operators(self):
        assert in_op([1], 1)
        assert not_in_op([2], 1)
        assert contains_op(1, [1])
        assert not_contains_op(1, [2])
        for func in (in_op, not_in_op, contains_op, not_contains_op):
            assert func(None, 1) is False
        assert and_op(True, "x") == "x"
        assert or_op(False, "x") == "x"


class TestMagicResolver:
    def test_ilter_and_extend(self):
        wrapped = MagicFilter.ilter(F.cast(int))
        assert wrapped("5") == 5

    def test_private_attr_and_len(self):
        with pytest.raises(AttributeError):
            _ = F._private
        with pytest.raises(TypeError, match="len"):
            len(F)
        assert F.cast(int)._replace_last(CastOperation(str)).resolve(1) == "1"

    def test_getitem_selector_and_key(self):
        assert F["x"].resolve({"x": 1}) == 1
        assert F[F.cast(bool)].resolve(1) == 1

    def test_getitem_switches_collection_mode(self):
        assert F[:].cast(bool).resolve([1, 0]) is False
        assert F[...].cast(bool).resolve([0, 2]) is True

    def test_invert_exclude_and_regular(self):
        f = ~F
        assert isinstance(f, MagicFilter)
        excluded = MagicFilter(
            operations=(
                ImportantFunctionOperation(
                    operator.not_,
                ),
            )
        )
        assert (~excluded).resolve(0) == 0
        assert (~F.cast(bool)).resolve(0) is True

    def test_comparators(self):
        cases = [
            (lambda f: f == 1, 1, True),
            (lambda f: f != 1, 1, False),
            (lambda f: f < 2, 1, True),
            (lambda f: f > 2, 1, False),
            (lambda f: f <= 2, 1, True),
            (lambda f: f >= 2, 1, False),
        ]
        for make_filter, value, expected in cases:
            assert make_filter(F).resolve(value) is expected

    def test_call_and_bool_operators(self):
        assert F()(2).resolve(2) is None
        assert (F & True).resolve(1) == 1
        assert (True & F).resolve(1) == 1
        assert not (F | False).resolve(0)
        assert not (False | F).resolve(0)
        assert not (F ^ True).resolve(1)
        assert not (True ^ F).resolve(1)
        assert (F & F).resolve(2) == 2
        assert (F | F).resolve(2) == 2

    @pytest.mark.parametrize(
        "make_filter,expected",
        [
            (lambda f: f >> 2, 1),
            (lambda f: 2 >> f, 0),
            (lambda f: f << 2, 16),
            (lambda f: 2 << f, 32),
            (lambda f: f + 2, 6),
            (lambda f: 2 + f, 6),
            (lambda f: f - 2, 2),
            (lambda f: 2 - f, -2),
            (lambda f: f * 2, 8),
            (lambda f: 2 * f, 8),
            (lambda f: f / 2, 2.0),
            (lambda f: 2 / f, 0.5),
            (lambda f: f // 2, 2),
            (lambda f: 2 // f, 0),
            (lambda f: f % 2, 0),
            (lambda f: 2 % f, 2),
            (lambda f: f**2, 16),
            (lambda f: 2**f, 16),
        ],
    )
    def test_arithmetic_operators(self, make_filter, expected):
        assert make_filter(F).resolve(4) == expected

    def test_matmul(self):
        matrix = Matrix()
        assert (F @ 2).resolve(matrix) == "matrix-product"
        assert (2 @ F).resolve(matrix) == "r-matrix-product"

    def test_unary_and_identity(self):
        assert (+F).resolve(1) == 1
        assert (-F).resolve(1) == -1
        assert F.is_(1).resolve(1) is True
        assert F.is_not(2).resolve(1) is True
        assert F.in_([1]).resolve(1) is True
        assert F.not_in([1]).resolve(1) is False
        assert F.contains(1).resolve([1]) is True
        assert F.not_contains(1).resolve([1]) is False
        assert F.len().resolve([1]) == 1

    def test_regexp_modes(self):
        assert F.regexp(r"\d+").resolve("123")
        assert F.regexp(r"x", mode="search").resolve("xyz")
        with pytest.warns(DeprecationWarning):
            assert F.regexp(r"x", search=True).resolve("x")
        import warnings

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            with pytest.raises(ParamsConflict):
                F.regexp(r"x", search=True, mode="match")

    def test_func_cast_extract_attr_dict_and_strings(self):
        assert F.func(lambda x: x + 1).resolve(1) == 2
        assert F.cast(int).resolve("4") == 4
        assert F.extract(F.cast(bool)).resolve([True, False]) == [True]
        obj = F.attr_dict.resolve({"a": 1})
        assert isinstance(obj, AttrDict)
        assert F.lower().resolve("ABC") == "abc"
        assert F.upper().resolve("abc") == "ABC"
        assert F.title().resolve("hello world") == "Hello World"
        assert F.capitalize().resolve("hello") == "Hello"

    def test_as_and_cast(self):
        assert F.as_("answer").resolve("0") == {"answer": "0"}
        assert F.cast(int).as_("value").resolve("0") == {"value": 0}
