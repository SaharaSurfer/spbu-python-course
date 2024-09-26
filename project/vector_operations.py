from typing import List
from math import sqrt, acos

from project.matrix_operations import Matrix


class Vector(Matrix):
    """
    A class to represent a vector, inheriting from the Matrix class.
    It provides additional functionality specific to vectors, such as calculating
    the vector's magnitude, dot product, and angle between vectors.

    Methods:
    -------
    `length() -> float`:
        Returns the magnitude (length) of the vector.

    `dot_product(a: "Vector", b: "Vector") -> float`:
        Static method to calculate the dot product of two vectors.

    `angle(a: "Vector", b: "Vector") -> float`:
        Static method to calculate the angle (in radians) between two vectors.

    `is_vector(list_of_lists: List[List[float]]) -> bool`:
        Static method to check if the input is a valid vector.
    """

    def __init__(self, list_of_lists: List[List[float]]) -> None:
        """
        Initializes a Vector object.
        """

        super().__init__(list_of_lists)

        if not Vector.is_vector(list_of_lists):
            raise TypeError("Input must be a valid vector.")

    def length(self) -> float:
        """
        Returns the magnitude (length) of the vector.
        """

        # __len__ can't be used because it must return int
        return sqrt(sum(val**2 for row in self._matrix for val in row))

    @staticmethod
    def dot_product(a: "Vector", b: "Vector") -> float:
        """
        Calculates the dot product of two vectors.
        """

        if not a._has_same_dimension(b):
            raise ValueError("Vectors have incompatible dimensions.")

        return sum(
            a._matrix[row_ind][col_ind] * b._matrix[row_ind][col_ind]
            for row_ind in range(len(a._matrix))
            for col_ind in range(len(a._matrix[0]))
        )

    @staticmethod
    def angle(a: "Vector", b: "Vector") -> float:
        """
        Calculates the angle (in radians) between two vectors.
        """

        return acos(Vector.dot_product(a, b) / (a.length() * b.length()))

    @staticmethod
    def is_vector(list_of_lists: List[List[float]]) -> bool:
        """
        Checks if the input is a valid vector (1xN or Nx1 matrix).
        """

        return len(list_of_lists) == 1 or all(
            len(row) == 1 for row in list_of_lists
        )
