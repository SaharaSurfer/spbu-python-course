import copy
from typing import Callable, Any
from functools import wraps
from inspect import signature


class Evaluated:
    """
    A marker class that delays the evaluation of a functionp passed.
    The function is stored and only executed when the `evaluate()` method is invoked.

    This is useful in scenarios where you want to pass a function as an argument and control
    when it is executed, rather than evaluating it immediately upon being passed.

    Args:
        func: A function to be wrapped and delayed for evaluation.

    Raises:
        ValueError: If the function is already an instance of or derived from the `Isolated` class.
    """

    def __init__(self, func: Callable[..., Any]) -> None:
        if (
            isinstance(func, Isolated)
            or isinstance(func, type)
            and issubclass(func, Isolated)
        ):
            raise ValueError(
                "It is not possible to use Isolated and Evaluated in conjunction with each other"
            )

        self.__func = func

    def evaluate(self) -> Any:
        """
        Evaluates the stored function and returns its result.

        Returns:
            The result of the stored function execution.
        """

        return self.__func()


class Isolated:
    """
    A marker class used to indicate that a function argument should be deeply copied
    when passed into the function. It ensures that changes made to the argument inside
    the function do not affect the original value passed in.

    This class has no behavior by itself but serves as a flag to indicate isolation for arguments.
    """

    def __init__(self) -> None:
        pass


def smart_args(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    A decorator that applies special behavior to function arguments based on their types.

    - Arguments with default values of type `Isolated` are deeply copied to ensure isolation.
    - Arguments with default values of type `Evaluated` are lazily evaluated only when needed.

    Args:
        func: The function to be wrapped with smart argument handling.

    Returns:
        A wrapped function where special handling for `Isolated` and `Evaluated` arguments is applied.

    Raises:
        ValueError: If invalid argument types are passed to the function.
    """

    sig = signature(func)

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        """
        The wrapped function that processes arguments based on their type.

        - Deep copies `Isolated` arguments to avoid mutation.
        - Lazily evaluates `Evaluated` arguments if not explicitly provided in `kwargs`.

        Args:
            *args: Positional arguments for the function.
            **kwargs: Keyword arguments for the function.

        Returns:
            The result of the original function after processing arguments.
        """

        # Apply given arguments and set default for missing ones
        bound_args = sig.bind_partial(*args, **kwargs)
        bound_args.apply_defaults()

        # Iterate through the bound arguments
        for name, value in bound_args.arguments.items():
            # Get the parameter by the name
            param = sig.parameters[name]

            # Process it depending on default value
            if isinstance(param.default, Isolated):
                if name in kwargs and value != param.default:
                    bound_args.arguments[name] = copy.deepcopy(value)
                else:
                    raise TypeError(
                        "Invalid scenario of using the 'Isolated' class"
                    )

            elif isinstance(param.default, Evaluated):
                if name not in kwargs and value == param.default:
                    bound_args.arguments[name] = param.default.evaluate()
                elif name in kwargs and value != param.default:
                    pass  # We don''t need to modify value here
                else:
                    raise TypeError(
                        "Invalid scenario of using the 'Evaluated' class"
                    )

        # Call the original function with updated arguments
        return func(*bound_args.args, **bound_args.kwargs)

    return wrapper
