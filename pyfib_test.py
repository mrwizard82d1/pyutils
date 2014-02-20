"""Implements unit tests for the pyfib module."""


import unittest2

import pyfib

__author__ = 'ljones'


class PyFibTest(unittest2.TestCase):
    """Defines the unit tests for the pyfib module."""

    def test_when_fibs_below_0_then_empty_sequence_returned(self):
        self.assertEqual(0, len(list(pyfib.fibs_below(0))))

    def test_when_fibs_below_1_then_empty_sequence_returned(self):
        self.assertEqual([], list(pyfib.fibs_below(1)))

    def test_when_fibs_below_2_then_correct_sequence_returned(self):
        self.assertEqual([1, 1], list(pyfib.fibs_below(2)))

    def test_when_fibs_below_3_then_correct_sequence_returned(self):
        self.assertEqual([1, 1, 2], list(pyfib.fibs_below(3)))

    def test_when_fibs_below_100_then_correct_sequence_returned(self):
        self.assertEqual([1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89],
                         list(pyfib.fibs_below(100)))


def suite():
    """Return the suite of unit tests from this module."""
    result = unittest2.TestSuite();
    result.addTest(unittest2.makeSuite(PyFibTest))
    return result


if __name__ == '__main__':
    unittest2.main()