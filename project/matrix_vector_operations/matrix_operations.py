from typing import List
from math import sumprod
from itertools import batched, starmap, product


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

        self.height = len(self._matrix)
        self.width = len(self._matrix[0])

    def transpose(self) -> "Matrix":
        """
        Transposes the matrix (flips rows and columns).
        """

        return Matrix(list(map(list, zip(*self._matrix))))

    def __iadd__(self, other: "Matrix") -> "Matrix":
        """
        Performs in-place matrix addition (self += other).
        """

        if not self._has_same_dimension(other):
            raise ValueError("Matrix 'other' has wrong dimension.")

        # 1 way
        self._matrix = [
            [
                self._matrix[i][j] + other._matrix[i][j]
                for j in range(self.width)
            ]
            for i in range(self.height)
        ]

        return self

    def __add__(self, other: "Matrix") -> "Matrix":
        """
        Adds two matrices and returns a new matrix.
        """

        if not self._has_same_dimension(other):
            raise ValueError("Matrix 'other' has wrong dimension.")

        # 2 way
        return Matrix(
            [
                [a + b for a, b in zip(row_1, row_2)]
                for row_1, row_2 in zip(self._matrix, other._matrix)
            ]
        )

    def __mul__(self, other: "Matrix") -> "Matrix":
        """
        Multiplies two matrices and returns a new matrix.
        """

        if not self._is_multiplicable(other):
            raise ValueError(f"Matrices can't be multiplied.")

        return Matrix(
            list(
                map(
                    list,
                    batched(
                        starmap(
                            sumprod, product(self._matrix, zip(*other._matrix))
                        ),
                        other.width,
                    ),
                )
            )
        )

    def _has_same_dimension(self, other: "Matrix") -> bool:
        """
        Checks if two matrices have the same dimensions.
        """

        return self.height == other.height and self.width == other.width

    def _is_multiplicable(self, other: "Matrix") -> bool:
        """
        Checks if two matrices can be multiplied (i.e., the number of columns
        in the first matrix is equal to the number of rows in the second).
        """

        return self.width == other.height

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
