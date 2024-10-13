import pytest
from typing import Any
from itertools import count

from project.decorators.smart_args import smart_args, Isolated, Evaluated

# Helper function to simulate unique values
counter = count()


def get_unique_value() -> int:
    return next(counter)


class TestSmartArgs:
    def test_isolated(self) -> None:
        """Test that Isolated prevents mutations across invocations."""

        @smart_args
        def check_isolation(*, d: Any = Isolated()) -> Any:
            d["a"] = 0
            return d

        # Initial dict
        no_mutable = {"a": 10}

        # Call the function with Isolated
        result = check_isolation(d=no_mutable)

        # Ensure the Isolated behavior (no side effects on the original dict)
        assert result == {"a": 0}
        assert no_mutable == {"a": 10}

    def test_evaluated(self) -> None:
        """Test that Evaluated computes the default value only once."""

        @smart_args
        def check_evaluation(*, x: int = get_unique_value(), y: int = Evaluated(get_unique_value)) -> tuple[int, int]:  # type: ignore
            return x, y

        result1 = check_evaluation()
        result2 = check_evaluation()
        result3 = check_evaluation(y=150)

        assert (
            result1[0] == result2[0] == result3[0]
        )  # x should be the same across all calls
        assert result1[1] != result2[1]  # y should differ between calls
        assert (
            result3[1] == 150
        )  # If y is explicitly set, it should not evaluate the default

    def test_isolated_and_evaluated_in_combination(self) -> None:
        """Test that Isolated(Evaluated(func)) and Evaluated(Isolated) combinations are prohibited."""
        # Test Isolated inside Evaluated
        with pytest.raises(
            ValueError,
            match="It is not possible to use Isolated and Evaluated in conjunction with each other",
        ):

            @smart_args
            def check_isolated_in_evaluated(
                *, a: Any = Evaluated(Isolated)
            ) -> Any:
                return a

        with pytest.raises(
            ValueError,
            match="It is not possible to use Isolated and Evaluated in conjunction with each other",
        ):

            @smart_args
            def check_isolated_in_evaluated(*, a: Any = Evaluated(Isolated())) -> Any:  # type: ignore
                return a

        # Test Evaluated inside Isolated
        with pytest.raises(TypeError):

            @smart_args
            def check_evaluated_in_isolated(*, b: Any = Isolated(Evaluated(get_unique_value))) -> Any:  # type: ignore
                return b

    def test_isolated_with_positional_argument(self) -> None:
        """Test that Isolated works correctly with positional arguments passed by key."""

        @smart_args
        def check_isolated_positional(d: Any = Isolated()) -> Any:
            d["a"] = 0
            return d

        no_mutable = {"a": 10}
        result = check_isolated_positional(d=no_mutable)

        assert result == {"a": 0}
        assert no_mutable == {"a": 10}  # Ensure original is not mutated

    def test_evaluated_with_positional_argument(self) -> None:
        """Test that Evaluated works correctly with positional arguments passed by key."""

        @smart_args
        def check_evaluated_positional(
            b: Any = Evaluated(get_unique_value),
        ) -> Any:
            return b

        result1 = check_evaluated_positional()
        result2 = check_evaluated_positional()

        assert result1 != result2
