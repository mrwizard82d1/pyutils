#! env python


"""Defines and executes unit tests for the path2list module."""


import unittest

import path2list


class Path2ListTest(unittest.TestCase):
    """Defines the unit tests for the path2list module."""

    def testEmptyPathProducesEmptyStr(self):
        """Convert an empty path returns an empty string."""
        self.assertEqual('', path2list.path2list(''))

    def testOneItemProducesSingleItem(self):
        """Convert a single item path returns a single item string."""
        self.assertEqual('auris', path2list.path2list('auris'))

    def testManyItemsProducesItemList(self):
        """Convert a many-item path to a many-item string."""
        self.assertEqual('declivitate\nlitteratum\n' +
                         'farciunt\nle_bouleversement',
            path2list.path2list('declivitate;litteratum;' +
                                'farciunt;le_bouleversement'))
                         

def suite():
    """Returns the suite of unit tests for this module."""
    return unittest.makeSuite(Path2ListTest, 'test')


if __name__ == '__main__':
    unittest.main()
