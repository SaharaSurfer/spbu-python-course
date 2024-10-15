from typing import Callable, Any


def curry_explicit(
    function: Callable[..., Any], arity: int
) -> Callable[..., Any]:
    """
    Converts a function into a curried form with a specified number of arguments (arity).
    Currying allows a function with multiple arguments to be called one argument at a time.

    Args:
        function: The function to be curried.
        arity: The number of arguments (arity) required by the function.

    Returns:
        A curried version of the function that can be invoked one argument at a time
        until all arguments are provided.

    Raises:
        ValueError: If arity is negative, since the number of arguments must be non-negative.

    Example:
        >>> def add_three(a, b, c):
        ...     return a + b + c
        ...
        >>> curried_add = curry_explicit(add_three, 3)
        >>> curried_add(1)(2)(3)
        6
    """

    if arity < 0:
        raise ValueError("Arrity must be non-negative")

    if arity == 0:
        return function

    def helper(arg: Any) -> Any:
        """
        Helper function that accumulates arguments until the specified arity is reached.
        Once the number of collected arguments matches the arity, it calls the original function.

        Args:
            arg: A single argument provided to the curried function.

        Returns:
            Either the curried function expecting more arguments or the final result
            if the arity has been fulfilled.
        """

        current_arg_count = getattr(helper, "arg_count", 0)
        current_args: tuple[Any, ...] = getattr(
            helper, "collected_args", tuple()
        )

        if current_arg_count == arity - 1:
            return function(*current_args, arg)

        setattr(helper, "collected_args", current_args + (arg,))
        setattr(helper, "arg_count", current_arg_count + 1)

        return helper

    # Initialize the helper function's state.
    setattr(helper, "collected_args", tuple())
    setattr(helper, "arg_count", 0)

    return helper
