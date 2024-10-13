import math
from typing import Generator


def prime_num_gen() -> Generator[int, None, None]:
    """
    Generates an infinite sequence of prime numbers.

    This is a generator function that yields prime numbers indefinitely. It starts from 2
    (the smallest prime number) and checks each subsequent number for primality. A number
    is considered prime if it is not divisible by any number other than 1 and itself.
    The generator uses trial division up to the square root of the current number (`n`)
    to determine if it is prime.

    Yields:
        The next prime number in the sequence.

    Example:
    >>> gen = prime_num_gen()
    >>> next(gen)
    2
    >>> next(gen)
    3
    >>> next(gen)
    5
    >>> next(gen)
    7
    >>> next(gen)
    11
    """

    n = 2

    while True:
        is_prime = True
        limit = math.isqrt(n)

        for divisor in range(2, limit + 1):
            if n % divisor == 0:
                is_prime = False
                break

        if is_prime:
            yield n

        n += 1
