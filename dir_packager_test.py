#! env python


"""Defines and runs the unit tests for the dir_packager module."""


import os
import unittest
import shutil

import dir_packager


class DirPackagerNameTest(unittest.TestCase):
    """Defines the name unit tests for the .zip file packagers."""

    def testDirnameNoPkgName(self):
        """Verify package name correct when dirname supplied."""
        unzipper = dir_packager.Unzipper('le_cheque')
        self.assertEqual('le_cheque', unzipper.dirname)
        self.assertEqual('le_cheque.zip', unzipper.pkgFilename)

    def testDirnamePkgName(self):
        """Verify the dirname and package name are both set correctly."""
        unzipper = dir_packager.Unzipper('ripis', 'olerinis.zip', )
        self.assertEqual('olerinis.zip', unzipper.pkgFilename)
        self.assertEqual('ripis', unzipper.dirname)

    def testNoDirnameNoPkgName(self):
        """Verify the dirname and package name when none are supplied."""
        zipper = dir_packager.Zipper()
        self.assertEqual('', zipper.dirname)
        self.assertEqual('dir_package.zip', zipper.pkgFilename)

    def testNoDirnamePkgName(self):
        """Verify the dirname if only the package name if supplied."""
        filename = 'quaerunt.zip'
        unzipper = dir_packager.Unzipper(zipFilename=filename)
        self.assertEqual(os.path.splitext(filename)[0],
                         unzipper.dirname)
        self.assertEqual(filename, unzipper.pkgFilename)

    def testRootOnlyNoPkgname(self):
        """Verify the package name is correct if the dir is root."""
        zipper = dir_packager.Zipper('/')
        self.assertEqual('dir_package.zip', zipper.pkgFilename)
        self.assertEqual('/', zipper.dirname)
        
        
class ZipPackageTest(unittest.TestCase):
    """Defines unit tests for the .zip file packages."""

    def setUp(self):
        """Set up the test fixture."""

        # initialize members
        self._empty_dirname = 'nulla'
        self._empty_zipname = '{0}.zip'.format(self._empty_dirname)
        self._emptySubdirTree = ('necessaire',
                                 (('aqua',),
                                  ('voluisti',),
                                  ('reginae', tuple()),
                                  ('invetavi',)))

        # clean old fixtures
        self._cleanFixtures()
        
        # set up new fixtures
        os.mkdir(self._empty_dirname)
        self.makeTree(self._emptySubdirTree)

    def testZipEmptyDir(self):
        """Verify zipping an empty directory."""
        zipper = dir_packager.Zipper(self._empty_dirname)
        zipper.execute()
        self.assertTrue(os.path.isfile(zipper.pkgFilename))
        self.assertTrue(os.stat(zipper.pkgFilename).st_size > 0)
        os.rmdir(self._empty_dirname)
        unzipper = dir_packager.Unzipper(zipFilename=zipper.pkgFilename)
        unzipper.execute()
        self.assertTrue(os.path.isdir(self._empty_dirname))
        self.assertTrue(len(os.listdir(self._empty_dirname)) == 0)

##    def testZipEmptySubDirAmongFilesSkipsDir(self):
##        """Verify that zipper skips empty directory but zips files."""
##        zipper = dir_packager.Zipper(self._emptySubdirTree[0])
##        zipper.execute()
##        shutil.rmtree(self._emptySubdirTree[0])
##        unzipper = dir_packager.\
##                   Unzipper(zipFilename='{0}.zip'.
##                            format(self._emptySubdirTree[0]))
##        unzipper.execute()
##        self.verifyTree(self._emptySubdirTree, self._emptySubdirTree[0])

    def tearDown(self):
        """Tear down the test fixture."""
        self._cleanFixtures()

    def _cleanFixtures(self):
        """Remove all test fixtures from the OS filesystem."""
        if (os.path.isdir(self._empty_dirname)):
            os.rmdir(self._empty_dirname)
        if (os.path.isfile(self._empty_zipname)):
            os.remove(self._empty_zipname)
        emptySubdirTreeZipName = '{0}.zip'.format(self._emptySubdirTree[0])
        if (os.path.isfile(emptySubdirTreeZipName)):
            os.remove(emptySubdirTreeZipName)
        if (os.path.isdir(self._emptySubdirTree[0])):
            shutil.rmtree(self._emptySubdirTree[0])
        
    def makeTree(self, tree, root='.'):
        """Creates a directory tree."""
        # if root node has children
        if len(tree) > 1:
            # create a directory...
            root = os.path.join(root, tree[0])
            os.mkdir(root)
            # ...and fill it
            for subtree in tree[1]:
                self.makeTree(subtree, root)
        # otherwise no children
        else:
            # so just create a file
            pathname = os.path.join(root, tree[0])
            self.touchFile(pathname)

    def touchFile(self, filename):
        """Creates an empty file named filename."""
        f = open(filename, 'w')
        f.close()



def suite():
    """Returns the suite of unit tests in this module."""
    result = None
    return result


if __name__ == '__main__':
    unittest.main()
