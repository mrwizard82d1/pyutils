"""Unit tests for mapped_drives module."""


import unittest

from mapped_drives import MappedDrives


class MappedDrivesTest(unittest.TestCase):

    def setUp(self):
        self.manager = MappedDrives()

    def test_drives(self):
        expected_list = ['W:']
        self.assertEquals(expected_list, self.manager.drives())


def suite():
    """Return the suite of tests for this module."""
    return unittest.suite()


if __name__ == '__main__':
    unittest.main()
    
