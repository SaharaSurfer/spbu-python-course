import pytest
from typing import Any

from project.decorators.curry_explicit import curry_explicit


class TestCurryExplicit:
    def test_negative_arity(self) -> None:
        """Test that a negative arity raises an exception."""
        with pytest.raises(ValueError, match="Arrity must be non-negative"):
            curry_explicit(lambda x: x, -1)

    def test_too_many_arguments_at_once(self) -> None:
        """Test that passing more than one argument at a time raises an exception."""

        def add(a: int, b: int) -> int:
            return a + b

        curried_add = curry_explicit(add, 2)

        with pytest.raises(TypeError):
            curried_add(1, 2)  # Passing two arguments at once

    def test_too_many_total_arguments(self) -> None:
        """Test that passing more arguments than the specified arity raises an exception."""

        def add(a: int, b: int) -> int:
            return a + b

        curried_add = curry_explicit(add, 2)

        curried_partial = curried_add(1)
        with pytest.raises(TypeError):
            curried_partial(2)(3)  # Exceeding the arity

    def test_passed_arguments_less_than_arity(self) -> None:
        """Test that passing fewer arguments than expected allows partial application."""

        def add(a: int, b: int) -> int:
            return a + b

        curried_add = curry_explicit(add, 2)
        curried_partial = curried_add(1)
        result = curried_partial(2)
        assert result == 3

    def test_arity_zero(self) -> None:
        """Test that arity 0 works correctly with no arguments."""

        def no_args() -> str:
            return "no args"

        curried_no_args = curry_explicit(no_args, 0)
        assert curried_no_args() == no_args()

    def test_arity_one(self) -> None:
        """Test that arity 1 works correctly."""

        def single_arg(x: Any) -> str:
            return f"Arg: {x}"

        curried_single_arg = curry_explicit(single_arg, 1)
        result = curried_single_arg(42)
        assert result == single_arg(42)

    def test_arbitrary_arity_function(self) -> None:
        """Test that functions with arbitrary arity are frozen at the specified arity."""
        curried_max = curry_explicit(
            max, 3
        )  # We want to curry the max function with arity 3

        result = curried_max(5)(1)(10)  # Providing 3 arguments one at a time
        assert result == 10  # The maximum of (5, 1, 10) is 10

        with pytest.raises(TypeError):
            result(5)
