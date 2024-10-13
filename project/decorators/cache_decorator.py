from typing import Callable, Any
from llist import dllist, dllistnode  # type: ignore


def make_key(args: tuple[Any, ...], kwargs: dict[str, Any]) -> tuple[Any, ...]:
    """
    Generates a hashable cache key from the arguments passed to the function.
    Handles nested structures like dicts, lists, sets, and tuples by recursively
    converting them into sorted, immutable tuples.

    Args:
        args: Positional arguments of the function.
        kwargs: Keyword arguments of the function.

    Returns:
        A tuple that can be used as a unique key for the function call.
    """

    def recursive_convert(item: Any) -> Any:
        """
        Recursively converts mutable structures (like dicts, lists, sets)
        into immutable tuples to make them hashable for cache keys.

        Args:
            item: The item to be converted, which can be a dict, list, set, tuple, or any other object.

        Returns:
            An immutable version of the input.
        """

        if isinstance(item, dict):
            # Convert dictionary into a sorted tuple of key-value pairs
            return tuple(
                (k, recursive_convert(v)) for k, v in sorted(item.items())
            )
        elif isinstance(item, (list, set)):
            # Convert lists and sets to tuples
            return tuple(recursive_convert(i) for i in item)
        elif isinstance(item, tuple):
            # Process tuples recursively
            return tuple(recursive_convert(i) for i in item)
        else:
            return item

    conv_args: tuple[Any, ...] = recursive_convert(args)
    conv_kwargs: tuple[Any, ...] = recursive_convert(kwargs)

    return conv_args + conv_kwargs


def lru_cache(maxsize: int = 0) -> Callable[..., Any]:
    """
    A decorator that implements a Least Recently Used (LRU) caching mechanism.
    Caches function results based on their arguments and evicts the least recently used
    result when the cache exceeds the specified max size.

    Args:
        maxsize: The maximum number of results to cache.

    Returns:
        A decorator that adds LRU caching to a function.
    """

    def cache(function: Callable[..., Any]) -> Callable[..., Any]:
        """
        Inner cache decorator function that wraps the original function.

        Args:
            function: The function to be wrapped with LRU caching.

        Returns:
            The wrapped function with LRU caching enabled.
        """

        # Cache dictionary where keys are function arguments and
        # values are nodes in the doubly linked list
        cache_dict: dict[tuple[Any, ...], dllistnode] = {}

        # Doubly linked list to maintain the access order of cached results
        lst = dllist()

        def helper(*args: Any, **kwargs: Any) -> Any:
            """
            The helper function that replaces the original function. It caches
            results based on the function's arguments.

            Args:
                *args: Positional arguments of the function.
                **kwargs: Keyword arguments of the function.

            Returns:
                The cached result or the result computed by the function.
            """

            # Create a hashable key for the current function call
            key = make_key(args, kwargs)

            # Check if the result is already in the cache
            node = cache_dict.get(key, None)
            if node:
                # Move the accessed node to the front of the list to mark it as most recently used
                lst.remove(node)

                # Update the node's position in the linked list and cache dictionary
                binded_node = lst.appendleft(node)
                cache_dict[key] = binded_node

                return node.value[1]

            # Compute the result if not found in cache
            result = function(*args, **kwargs)

            # Evict least recently used if cache is full
            if lst.size == maxsize:
                cache_dict.pop(lst.pop()[0])

            # Add the new result to the front of the list
            binded_node = lst.appendleft((key, result))
            cache_dict[key] = binded_node

            return result

        # Expose internal cache and linked list for testing
        setattr(helper, "cache", cache_dict)
        setattr(helper, "order", lst)

        return helper

    return cache
