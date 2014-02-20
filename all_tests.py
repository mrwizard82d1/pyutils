#! env python


"""Invokes all the unit tests for the module."""

import unittest

import dir_archive_test
import path2listtest
import pyfib_test


def suite():
    """Returns the suite of unit tests."""
    suites = [dir_archive_test.suite(), path2listtest.suite(),
              pyfib_test.suite()]
    return unittest.TestSuite(suites)


if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())

