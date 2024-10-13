from typing import Generator, Callable, Any


def get_nth_element(
    func: Callable[[], Generator[Any, None, None]]
) -> Callable[..., Any]:
    """
    Returns a function that retrieves the nth element from a generator function.

    This function acts as a wrapper around a generator-producing function. It runs
    the generator and retrieves the element at the specified index `n` (1-based index).
    If `n` is greater than the number of elements in the generator or less than or
    equal to zero, it raises an `IndexError`.

    Args:
        func : A function that, when called, returns a generator yielding elements of any type.

    Returns:
    Callable[..., Any]:
        A function that takes an integer `n` and returns the nth element from the
        generator produced by `func`.

    Raises:
    IndexError: If `n` is less than or equal to zero or if the generator does not yield `n` elements.

    Example:
    >>> def simple_gen():
    ...     yield from range(10)
    >>> get_third = get_nth_element(simple_gen)
    >>> get_third(3)
    2
    """

    def helper(n: int) -> Any:
        if n <= 0:
            raise IndexError(f"The index must be greater than 0")

        gen = func()
        for i, element in enumerate(gen, start=1):
            if i == n:
                return element

        raise IndexError(f"Generator does not have {n} elements.")

    return helper
