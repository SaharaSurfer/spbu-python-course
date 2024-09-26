import pytest

from project.matrix_operations import Matrix


class TestMatrixOperations:
    def test_matrix_init(self) -> None:
        # Valid matrix
        matrix = Matrix([[1, 2], [3, 4]])
        assert matrix._matrix == [[1, 2], [3, 4]]

        # Invalid matrix (jagged)
        with pytest.raises(TypeError):
            Matrix([[1, 2], [3]])

        # Empty matrix
        with pytest.raises(TypeError):
            Matrix([])

        # Matrix with empty row
        with pytest.raises(TypeError):
            Matrix([[], [1, 2]])

    def test_matrix_addition(self) -> None:
        matrix1 = Matrix([[1, 2], [3, 4]])
        matrix2 = Matrix([[5, 6], [7, 8]])
        result = matrix1 + matrix2
        assert result._matrix == [[6, 8], [10, 12]]

        # Matrices with different dimensions
        matrix1 = Matrix([[1, 2], [3, 4]])
        matrix2 = Matrix([[5, 6, 7], [8, 9, 10]])
        with pytest.raises(ValueError):
            matrix1 + matrix2

    def test_matrix_inplace_addition(self) -> None:
        matrix1 = Matrix([[1, 2], [3, 4]])
        matrix2 = Matrix([[5, 6], [7, 8]])
        matrix1 += matrix2
        assert matrix1._matrix == [[6, 8], [10, 12]]

    def test_matrix_multiplication(self) -> None:
        matrix1 = Matrix([[1, 2], [3, 4]])
        matrix2 = Matrix([[2, 0], [1, 2]])
        result = matrix1 * matrix2
        assert result._matrix == [[4, 4], [10, 8]]

        # Test with large matrices
        matrix1 = Matrix([[i for i in range(100)] for _ in range(100)])
        matrix2 = Matrix([[i for i in range(100)] for _ in range(100)])
        result = matrix1 * matrix2
        assert len(result._matrix) == 100
        assert len(result._matrix[0]) == 100

        # Matrices with incompatible dimensions for multiplication
        matrix1 = Matrix([[1, 2]])
        matrix2 = Matrix([[3, 4], [5, 6], [7, 8]])
        with pytest.raises(ValueError):
            matrix1 * matrix2

    def test_matrix_transpose(self) -> None:
        matrix = Matrix([[1, 2], [3, 4], [5, 6]])
        transposed = matrix.transpose()
        assert transposed._matrix == [[1, 3, 5], [2, 4, 6]]

    def test_singleton_matrix(self) -> None:
        # 1x1 matrix (singleton)
        matrix1 = Matrix([[3]])
        matrix2 = Matrix([[4]])

        result_add = matrix1 + matrix2
        result_mul = matrix1 * matrix2

        assert result_add._matrix == [[7]]
        assert result_mul._matrix == [[12]]
