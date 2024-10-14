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

    gen = func()
    index = 0

    def helper(n: int) -> Any:
        nonlocal index

        if n < index + 1:
            raise IndexError(
                f"The element with this index does not exist or it has been passed through"
            )

        result = None
        while index != n:
            result = next(gen, None)

            if result is None:
                raise IndexError(f"Generator does not have {n} elements.")

            index += 1

        return result

    return helper
