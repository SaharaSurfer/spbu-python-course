from typing import List


class Matrix:
    """
    A class to represent a mathematical matrix and perform operations such as
    addition, multiplication, and transposition.

    Methods:
    -------
    `transpose() -> "Matrix"`:
        Returns the transpose of the matrix.

    `__iadd__(other: "Matrix") -> "Matrix"`:
        Performs in-place matrix addition.

    `__add__(other: "Matrix") -> "Matrix"`:
        Performs matrix addition and returns a new matrix.

    `__mul__(other: "Matrix") -> "Matrix"`:
        Performs matrix multiplication and returns a new matrix.

    `_has_same_dimension(other: "Matrix") -> bool`:
        Checks if two matrices have the same dimensions.

    `_is_multiplicable(other: "Matrix") -> bool`:
        Checks if two matrices can be multiplied.

    `is_matrix(list_of_lists: List[List[float]]) -> bool`:
        Static method to check if a 2D list is a valid matrix.

    `__str__() -> str`:
        Returns a string representation of the matrix.
    """

    def __init__(self, list_of_lists: List[List[float]]) -> None:
        """
        Initializes a Matrix object.
        """

        if not Matrix.is_matrix(list_of_lists):
            raise TypeError("Input must be a valid matrix.")

        self._matrix = list_of_lists

    def transpose(self) -> "Matrix":
        """
        Transposes the matrix (flips rows and columns).
        """

        return Matrix([list(new_row) for new_row in zip(*self._matrix)])

    def __iadd__(self, other: "Matrix") -> "Matrix":
        """
        Performs in-place matrix addition (self += other).
        """

        if not self._has_same_dimension(other):
            raise ValueError("Matrix 'other' has wrong dimension.")

        for i in range(len(self._matrix)):
            for j in range(len(self._matrix[0])):
                self._matrix[i][j] += other._matrix[i][j]

        return self

    def __add__(self, other: "Matrix") -> "Matrix":
        """
        Adds two matrices and returns a new matrix.
        """

        res = Matrix([row[:] for row in self._matrix])
        res += other
        return res

    def __mul__(self, other: "Matrix") -> "Matrix":
        """
        Multiplies two matrices and returns a new matrix.
        """

        if not self._is_multiplicable(other):
            raise ValueError(f"Matrices can't be multiplied.")

        new_matrix = [
            [0.0] * len(other._matrix[0]) for _ in range(len(self._matrix))
        ]

        for row_ind in range(len(self._matrix)):
            for col_ind in range(len(other._matrix[0])):
                for val_ind in range(len(other._matrix)):
                    new_matrix[row_ind][col_ind] += (
                        self._matrix[row_ind][val_ind]
                        * other._matrix[val_ind][col_ind]
                    )

        return Matrix(new_matrix)

    def _has_same_dimension(self, other: "Matrix") -> bool:
        """
        Checks if two matrices have the same dimensions.
        """

        return len(self._matrix) == len(other._matrix) and len(
            self._matrix[0]
        ) == len(other._matrix[0])

    def _is_multiplicable(self, other: "Matrix") -> bool:
        """
        Checks if two matrices can be multiplied (i.e., the number of columns
        in the first matrix is equal to the number of rows in the second).
        """

        return len(self._matrix[0]) == len(other._matrix)

    @staticmethod
    def is_matrix(list_of_lists: List[List[float]]) -> bool:
        """
        Checks if the input is a valid matrix (a 2D list with equal-length rows).
        """

        if not list_of_lists or not list_of_lists[0]:
            return False

        return all(len(row) == len(list_of_lists[0]) for row in list_of_lists)

    def __str__(self) -> str:
        """
        Returns a string representation of the matrix, with rows separated by newlines
        and elements separated by spaces.
        """

        return "\n".join([" ".join(map(str, row)) for row in self._matrix])
