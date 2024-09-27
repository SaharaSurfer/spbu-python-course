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

        # Addition with negative numbers
        matrix1 = Matrix([[1, -2], [-3, 4]])
        matrix2 = Matrix([[-5, 6], [7, -8]])
        result = matrix1 + matrix2
        assert result._matrix == [[-4, 4], [4, -4]]

        # Addition with zero matrices
        matrix1 = Matrix([[0, 0], [0, 0]])
        matrix2 = Matrix([[0, 0], [0, 0]])
        result = matrix1 + matrix2
        assert result._matrix == [[0, 0], [0, 0]]

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

        # Multiplication with singleton matrix
        matrix1 = Matrix([[3]])
        matrix2 = Matrix([[5]])
        result = matrix1 * matrix2
        assert result._matrix == [[15]]

        # Matrices with incompatible dimensions for multiplication
        matrix1 = Matrix([[1, 2]])
        matrix2 = Matrix([[3, 4], [5, 6], [7, 8]])
        with pytest.raises(ValueError):
            matrix1 * matrix2

    def test_matrix_transpose(self) -> None:
        matrix = Matrix([[1, 2], [3, 4], [5, 6]])
        transposed = matrix.transpose()
        assert transposed._matrix == [[1, 3, 5], [2, 4, 6]]

        # Transposing a square matrix
        matrix = Matrix([[1, 2], [3, 4]])
        transposed = matrix.transpose()
        assert transposed._matrix == [[1, 3], [2, 4]]

        # Transposing a singleton matrix
        matrix = Matrix([[7]])
        transposed = matrix.transpose()
        assert transposed._matrix == [[7]]
