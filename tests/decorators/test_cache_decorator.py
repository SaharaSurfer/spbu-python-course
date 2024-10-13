import pytest
from itertools import count
from typing import Any

from project.decorators.cache_decorator import lru_cache, make_key

# Helper function to simulate unique values
counter = count()


def get_unique_value() -> int:
    return next(counter)


class TestCacheAndMakeKey:
    @pytest.mark.parametrize(
        "args, kwargs, expected_key",
        [
            (([1, 2, 3],), {}, ((1, 2, 3),)),
            (
                ([1, 2, 3],),
                {"param": [4, 5, 6]},
                ((1, 2, 3), ("param", (4, 5, 6))),
            ),
            (({"a": 1, "b": [2, 3]},), {}, ((("a", 1), ("b", (2, 3))),)),
            (
                ({1, 2, 3},),
                {"param": {4, 5, 6}},
                ((1, 2, 3), ("param", (4, 5, 6))),
            ),
        ],
    )
    def test_make_key(
        self,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
        expected_key: tuple[Any, ...],
    ) -> None:
        """Test make_key function with various types of inputs."""
        key = make_key(args, kwargs)
        assert key == expected_key

    def test_cache_add_and_inspect_internals(self) -> None:
        """Test that items are added to the cache and inspect cache internals."""

        @lru_cache(maxsize=3)
        def add(a: int, b: int) -> int:
            return a + b

        # Add items to the cache
        assert add(1, 2) == 3
        assert add(3, 4) == 7
        assert add(5, 6) == 11

        # Inspect the internal cache state
        assert len(add.cache) == 3
        keys_in_cache = [node[0] for node in add.order]
        assert keys_in_cache == [
            (5, 6),  # Most recently added
            (3, 4),
            (1, 2),  # Least recently used
        ]

    def test_cache_move_to_front_internals(self) -> None:
        """Test that cached items are moved to the front of the cache on access."""

        @lru_cache(maxsize=3)
        def multiply(a: int, b: int) -> int:
            return a * b

        # Fill the cache
        assert multiply(2, 3) == 6  # Cache [(2, 3)]
        assert multiply(4, 5) == 20  # Cache [(4, 5), (2, 3)]
        assert multiply(6, 7) == 42  # Cache [(6, 7), (4, 5), (2, 3)]

        # Access (2, 3) and ensure it moves to the front
        assert multiply(2, 3) == 6

        # Inspect the internal cache state
        keys_in_cache = [node[0] for node in multiply.order]
        assert keys_in_cache == [
            (2, 3),  # Most recently accessed (moved to the front)
            (6, 7),
            (4, 5),  # Least recently used
        ]

    def test_cache_eviction_and_internals(self) -> None:
        """Test that items are evicted correctly and inspect cache internals."""

        @lru_cache(maxsize=2)
        def subtract(a: int, b: int) -> int:
            return a - b

        # Add items to the cache
        assert subtract(10, 5) == 5  # Cache [(10, 5)]
        assert subtract(20, 10) == 10  # Cache [(20, 10), (10, 5)]

        # Adding a third item should evict (10, 5) because maxsize=2
        assert subtract(30, 15) == 15  # Cache [(30, 15), (20, 10)]

        # Inspect the internal cache state
        assert len(subtract.cache) == 2
        keys_in_cache = [node[0] for node in subtract.order]
        assert keys_in_cache == [
            (30, 15),  # Most recently added
            (20, 10),  # Least recently used
        ]

        # Ensure that (10, 5) is not in the cache anymore
        assert (10, 5) not in subtract.cache
