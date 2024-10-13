import pytest

from project.generators.rgba_gen import get_nth_rgba_vec


class TestRGBAGen:
    @pytest.mark.parametrize(
        "index, expected",
        [
            (1, (0, 0, 0, 2)),  # First element
            (5, (0, 0, 0, 10)),  # Arbitrary element
        ],
    )
    def test_get_nth_rgba_vec(
        self, index: int, expected: tuple[int, int, int, int]
    ) -> None:
        result = get_nth_rgba_vec(index)

        assert result == expected

    @pytest.mark.parametrize("invalid_index", [-1])  # Negative index
    def test_invalid_index(self, invalid_index: int) -> None:
        """Test that invalid indices raise an IndexError in the decorated function."""
        with pytest.raises(IndexError):
            get_nth_rgba_vec(invalid_index)
