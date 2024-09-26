import pytest
from math import isclose, sqrt

from project.vector_operations import Vector


class TestVectorOperations:
    def test_vector_init(self) -> None:
        # Valid vector (1xN)
        vector = Vector([[1, 2, 3]])
        assert vector._matrix == [[1, 2, 3]]

        # Valid vector (Nx1)
        vector = Vector([[1], [2], [3]])
        assert vector._matrix == [[1], [2], [3]]

        # Invalid vector
        with pytest.raises(TypeError):
            Vector([[1, 2], [3, 4]])

        # Empty vector
        with pytest.raises(TypeError):
            Vector([])

        # Vector with an empty row
        with pytest.raises(TypeError):
            Vector([[]])

    def test_vector_length(self) -> None:
        vector = Vector([[3, 4]])
        assert isclose(vector.length(), 5)

        # Very large vector
        large_vector = Vector([[i for i in range(1000)]])
        length = large_vector.length()
        expected_length = sqrt(sum(i**2 for i in range(1000)))
        assert isclose(length, expected_length)

    def test_vector_dot_product(self) -> None:
        vector1 = Vector([[1, 2, 3]])
        vector2 = Vector([[4, 5, 6]])
        dot = Vector.dot_product(vector1, vector2)
        assert dot == 32

        # Vectors with incompatible dimensions for dot product
        vector1 = Vector([[1, 2]])
        vector2 = Vector([[3, 4, 5]])
        with pytest.raises(ValueError):
            Vector.dot_product(vector1, vector2)

    def test_vector_angle(self) -> None:
        vector1 = Vector([[1, 0]])
        vector2 = Vector([[0, 1]])
        angle = Vector.angle(vector1, vector2)
        assert isclose(angle, 1.5708, abs_tol=1e-4)  # Pi/2 radians

    def test_singleton_vector(self) -> None:
        # 1x1 vector (a single value)
        vector = Vector([[5]])
        assert isclose(vector.length(), 5)
