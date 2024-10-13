import pytest

from project.generators.get_nth_element import get_nth_element
from project.generators.prime_num_gen import prime_num_gen


class TestPrimeNumGen:
    @pytest.mark.parametrize(
        "index, expected_prime",
        [
            (1, 2),  # 1st prime number
            (500, 3571),  # 500th prime number
        ],
    )
    def test_prime_gen_non_decorated(
        self, index: int, expected_prime: int
    ) -> None:
        """Test non-decorated prime_gen to verify nth prime."""
        gen = prime_num_gen()
        result = None
        for i, prime in enumerate(gen, start=1):
            if i == index:
                result = prime
                break

        assert result == expected_prime

    @pytest.mark.parametrize(
        "index, expected_prime",
        [
            (1, 2),  # 1st prime number
            (500, 3571),  # 500th prime number
        ],
    )
    def test_prime_gen_decorated(
        self, index: int, expected_prime: int
    ) -> None:
        """Test the decorated prime_gen to verify nth prime."""
        decorated_gen = get_nth_element(prime_num_gen)
        assert decorated_gen(index) == expected_prime

    @pytest.mark.parametrize(
        "invalid_index", [-1, 0]  # Invalid negative index and zero
    )
    def test_invalid_index(self, invalid_index: int) -> None:
        """Test invalid indices raise IndexError in the decorated function."""
        with pytest.raises(IndexError):
            decorated_gen = get_nth_element(prime_num_gen)
            decorated_gen(invalid_index)
