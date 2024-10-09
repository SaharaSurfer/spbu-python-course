import pytest
from math import isclose, pi

from project.matrix_vector_operations.vector_operations import Vector


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

        # Zero vector length
        zero_vector = Vector([[0, 0, 0]])
        assert isclose(zero_vector.length(), 0)

        # Singleton vector length (1x1 matrix)
        singleton_vector = Vector([[7]])
        assert isclose(singleton_vector.length(), 7)

    def test_vector_dot_product(self) -> None:
        vector1 = Vector([[1, 2, 3]])
        vector2 = Vector([[4, 5, 6]])
        dot = Vector.dot_product(vector1, vector2)
        assert dot == 32

        # Dot product of orthogonal vectors
        vector1 = Vector([[1, 0]])
        vector2 = Vector([[0, 1]])
        dot = Vector.dot_product(vector1, vector2)
        assert dot == 0

        # Vectors with incompatible dimensions for dot product
        vector1 = Vector([[1, 2]])
        vector2 = Vector([[3, 4, 5]])
        with pytest.raises(ValueError):
            Vector.dot_product(vector1, vector2)

        # Dot product of negative numbers
        vector1 = Vector([[-1, -2, -3]])
        vector2 = Vector([[-4, -5, -6]])
        dot = Vector.dot_product(vector1, vector2)
        assert dot == 32

    def test_vector_angle(self) -> None:
        vector1 = Vector([[1, 0]])
        vector2 = Vector([[0, 1]])
        angle = Vector.angle(vector1, vector2)
        assert isclose(angle, pi / 2, abs_tol=1e-4)

        # Parallel vectors
        vector1 = Vector([[1, 0]])
        vector2 = Vector([[2, 0]])
        angle = Vector.angle(vector1, vector2)
        assert isclose(angle, 0, abs_tol=1e-4)

        # Antiparallel vectors
        vector1 = Vector([[1, 0]])
        vector2 = Vector([[-1, 0]])
        angle = Vector.angle(vector1, vector2)
        assert isclose(angle, pi, abs_tol=1e-4)
