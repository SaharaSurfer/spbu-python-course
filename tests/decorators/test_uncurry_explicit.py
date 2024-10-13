import pytest
from typing import Callable, Any

from project.decorators.uncurry_explicit import uncurry_explicit


class TestUncurryExplicit:
    def test_negative_arity(self) -> None:
        """Test that a negative arity raises an exception."""
        with pytest.raises(ValueError, match="Arrity must be non-negative"):
            uncurry_explicit(lambda x: x, -1)

    def test_too_many_arguments(self) -> None:
        """Test that passing more arguments than the specified arity raises an exception."""

        def add(a: int) -> Callable[[int], int]:
            return lambda b: a + b

        uncurry_add = uncurry_explicit(add, 2)

        with pytest.raises(
            ValueError,
            match="Arity is inconsistent with the number of arguments given",
        ):
            uncurry_add(1, 2, 3)

    def test_passed_arguments_less_than_arity(self) -> None:
        """Test that passing fewer arguments than expected raises an exception."""

        def add(a: int) -> Callable[[int], int]:
            return lambda b: a + b

        uncurry_add = uncurry_explicit(add, 2)

        with pytest.raises(
            ValueError,
            match="Arity is inconsistent with the number of arguments given",
        ):
            uncurry_add(1)

    def test_arity_zero(self) -> None:
        """Test that arity 0 works correctly with no arguments."""

        def no_args() -> str:
            return "no args"

        uncurry_no_args = uncurry_explicit(no_args, 0)
        result = uncurry_no_args()
        assert result == no_args()

    def test_arity_one(self) -> None:
        """Test that arity 1 works correctly."""

        def single_arg(x: Any) -> str:
            return f"Arg: {x}"

        uncurry_single_arg = uncurry_explicit(single_arg, 1)
        result = uncurry_single_arg(42)
        assert result == single_arg(42)

    def test_arbitrary_arity_function(self) -> None:
        """Test that arbitrary arity functions are correctly handled."""

        def add(a: int) -> Callable[[int], Callable[[int], int]]:
            return lambda b: lambda c: a + b + c

        uncurry_add = uncurry_explicit(add, 3)
        result = uncurry_add(1, 2, 3)
        assert result == 6
