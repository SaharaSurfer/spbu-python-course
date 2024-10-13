from typing import Generator
from itertools import product


def get_rgba_gen() -> Generator[tuple[int, int, int, int], None, None]:
    """
    Generates all possible RGBA color combinations.

    This generator produces tuples representing all possible combinations of RGB values
    (with each component ranging from 0 to 255) and an alpha value (ranging from 0 to 100,
    but only even values are considered).

    The output is in the format (R, G, B, A), where:
    - R: Red component (0-255)
    - G: Green component (0-255)
    - B: Blue component (0-255)
    - A: Alpha transparency component (0, 2, 4, ..., 100)

    Yields:
    tuple[int, int, int, int]
        A tuple representing an RGBA color (R, G, B, A).

    Example:
    >>> gen = get_rgba_gen()
    >>> next(gen)
    (0, 0, 0, 0)
    >>> next(gen)
    (0, 0, 0, 2)
    >>> next(gen)
    (0, 0, 0, 4)
    """

    return (
        (r, g, b, a)
        for r, g, b in product(range(256), repeat=3)
        for a in range(0, 101)
        if a % 2 == 0
    )


def get_nth_rgba_vec(n: int) -> tuple[int, int, int, int]:
    """
    Retrieves the nth RGBA vector from the RGBA generator.

    This function uses the `get_rgba_gen()` generator to retrieve the RGBA color tuple at
    the specified index `n`. The index is 0-based, meaning the first element corresponds
    to `n=0`. If `n` is negative, it raises an `IndexError`.

    Args:
        n : The 0-based index of the RGBA tuple to retrieve.

    Returns:
    tuple[int, int, int, int]:
        The RGBA tuple at the specified index `n`.

    Raises:
    IndexError:
        If `n` is negative, or if the index exceeds the number of elements that can be generated.

    Example:
    >>> get_nth_rgba_vec(0)
    (0, 0, 0, 0)
    >>> get_nth_rgba_vec(1)
    (0, 0, 0, 2)
    >>> get_nth_rgba_vec(5)
    (0, 0, 0, 10)
    """

    if n < 0:
        raise IndexError("`n` must be non-negative")

    gen = get_rgba_gen()

    for i, val in enumerate(gen):
        if i == n:
            return val

    raise IndexError(f"Generator does not have {n} elements.")
