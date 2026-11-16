import math
from collections.abc import Callable
from functools import partial
from timeit import timeit


def num_digits(n: int) -> int:
    """
    Find the number of digits in a number.

    >>> num_digits(12345)
    5
    >>> num_digits(123)
    3
    >>> num_digits(0)
    1
    >>> num_digits(-1)
    1
    >>> num_digits(-123456)
    6
    >>> num_digits('123')  # Raises a TypeError for non-integer input
    Traceback (most recent call last):
        ...
    TypeError: Input must be an integer
    """
    if not isinstance(n, int):
        raise TypeError("Input must be an integer")

    digits = 0
    n = abs(n)
    while True:
        n = n // 10
        digits += 1
        if n == 0:
            break
    return digits


def num_digits_fast(n: int) -> int:
    """
    Find the number of digits in a number.
    abs() is used as logarithm for negative numbers is not defined.

    >>> num_digits_fast(12345)
    5
    >>> num_digits_fast(123)
    3
    >>> num_digits_fast(1000)
    4
    >>> num_digits_fast(10**15)
    16
    >>> num_digits_fast(0)
    1
    >>> num_digits_fast(-1)
    1
    >>> num_digits_fast(-123456)
    6
    >>> num_digits_fast('123')  # Raises a TypeError for non-integer input
    Traceback (most recent call last):
        ...
    TypeError: Input must be an integer
    """
    if not isinstance(n, int):
        raise TypeError("Input must be an integer")
    return 1 if n == 0 else math.floor(math.log10(abs(n)) + 1)


def num_digits_faster(n: int) -> int:
    """
    Find the number of digits in a number.
    abs() is used for negative numbers.

    Converting an integer to a string can raise ValueError when it exceeds
    Python's configured integer-string conversion limit (4300 digits by default).

    >>> num_digits_faster(12345)
    5
    >>> num_digits_faster(123)
    3
    >>> num_digits_faster(0)
    1
    >>> num_digits_faster(-1)
    1
    >>> num_digits_faster(-123456)
    6
    >>> num_digits_faster('123')  # Raises a TypeError for non-integer input
    Traceback (most recent call last):
        ...
    TypeError: Input must be an integer
    """
    if not isinstance(n, int):
        raise TypeError("Input must be an integer")

    return len(str(abs(n)))


def benchmark() -> None:
    """
    Compare digit-counting functions at three integer sizes.

    Timings are reported per call and vary by machine and Python version.

    >>> benchmark()  # doctest: +ELLIPSIS
    num_digits(19 bits): 6 digits, ... seconds per call
    num_digits_fast(19 bits): 6 digits, ... seconds per call
    num_digits_faster(19 bits): 6 digits, ... seconds per call
    <BLANKLINE>
    num_digits(51 bits): 16 digits, ... seconds per call
    num_digits_fast(51 bits): 16 digits, ... seconds per call
    num_digits_faster(51 bits): 16 digits, ... seconds per call
    <BLANKLINE>
    num_digits(101 bits): 31 digits, ... seconds per call
    num_digits_fast(101 bits): 31 digits, ... seconds per call
    num_digits_faster(101 bits): 31 digits, ... seconds per call
    <BLANKLINE>
    """

    def benchmark_a_function(func: Callable[[int], int], value: int) -> None:
        iterations = 100_000
        timing = timeit(partial(func, value), number=iterations)
        print(
            f"{func.__name__}({value.bit_length()} bits): {func(value)} digits, "
            f"{timing / iterations:.9f} seconds per call"
        )

    for value in (262144, 1125899906842624, 1267650600228229401496703205376):
        for func in (num_digits, num_digits_fast, num_digits_faster):
            benchmark_a_function(func, value)
        print()


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
