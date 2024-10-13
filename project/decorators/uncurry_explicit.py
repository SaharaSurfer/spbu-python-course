from typing import Callable, Any


def uncurry_explicit(
    function: Callable[..., Any], arity: int
) -> Callable[..., Any]:
    """
    Transforms a curried function into an uncurried form that takes all arguments at once.

    A curried function is one that takes multiple arguments one at a time. This function
    transforms such a function into one that takes all its arguments in a single call.

    Args:
        function: The curried function to be transformed.
        arity: The number of arguments the function expects.

    Returns:
        A new function that takes `arity` arguments all at once, instead of one by one.

    Raises:
        ValueError: If `arity` is negative or if the number of provided arguments
                    is inconsistent with the expected arity.

    Example:
        >>> def curried_add(a):
        ...     return lambda b: lambda c: a + b + c
        ...
        >>> uncurried_add = uncurry_explicit(curried_add, 3)
        >>> uncurried_add(1, 2, 3)
        6
    """

    if arity < 0:
        raise ValueError("Arrity must be non-negative")

    def helper(*args: Any) -> Any:
        """
        The helper function that accepts all arguments at once, validates the number of arguments,
        and then applies them to the curried function step by step.

        Args:
            *args: The arguments to be passed to the uncurried function.

        Returns:
            The result of the original function after all arguments have been applied.

        Raises:
            ValueError: If the number of arguments provided is inconsistent with the expected arity.
        """

        if len(args) != arity:
            raise ValueError(
                "Arity is inconsistent with the number of arguments given"
            )

        if not args:
            return function()

        result = function
        for arg in args:
            result = result(arg)

        return result

    return helper
