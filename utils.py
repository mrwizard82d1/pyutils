"""Miscellaneous utilities."""


__author__ = 'ljones'


def to_hex(value, bit_count):
    """Converts an integer to a hexadecimal values with bit_count bits."""

    return hex((value + (1 << bit_count)) % (1 << bit_count))

