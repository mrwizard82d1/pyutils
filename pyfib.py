"""Implements utilities related to Fibonacci numbers."""


__author__ = 'ljones'


def fibs_below(n):
    if n < 1:
        raise StopIteration()

    a = b = 1
    while a < n:
        yield a
        a, b = b, a + b