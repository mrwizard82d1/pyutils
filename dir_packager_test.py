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
        self._contentTree = {'la_station' : ['scirit', 'possible'],
                             'possible' : ['publici', 'existit'],
                             'publici' : ['stipat', 'porcus',
                                          'elephanti', 'ultimo']}
        self._contentTreeRoot = 'la_station'
        self._content = {'scirit' : 'tellus. Phasellus posuere,',
                         'existit' : 'sit',
                         'porcus' : 'rutrum risus. Nullam consectetur',
                         'elephanti' : 'Nam pretium justo nec magna',
                         'ultimo' : 'odio'}
        self._empty_dirname = 'nulla'
        self._empty_zipname = '{0}.zip'.format(self._empty_dirname)
        self._emptyTree = {'necessaire' : ['aqua', 'voluisti',
                                           'reginae', 'invetavi'],
                           'reginiae' : []}
        self._emptyTreeRoot = 'necessaire'

        # clean old fixtures
        self._cleanFixtures()
        
        # set up new fixtures
        os.mkdir(self._empty_dirname)
        self.makeTree(self._emptyTree, self._emptyTreeRoot)
        self.makeTree(self._contentTree, self._contentTreeRoot,
                      content=self._content)

    def testUnzipHasCorrectTimeStamps(self):
        """Verify that unzipping a subdirectory restores time stamps."""
        self.fail()

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

    def testZipEmptySubDirAmongFilesSkipsDir(self):
        """Verify that zipper skips empty directory but zips files."""
        zipper = dir_packager.Zipper(self._emptyTreeRoot)
        zipper.execute()
        shutil.rmtree(self._emptyTreeRoot)
        unzipper = dir_packager.Unzipper(zipFilename=zipper.pkgFilename)
        unzipper.execute()
        self.verifyTree(self._emptyTree)

    def testZipSubdirZipsFileContent(self):
        """Verify that zipping a subdirectory zips file content."""
        zipper = dir_packager.Zipper(self._contentTreeRoot)
        zipper.execute()
        shutil.rmtree(self._contentTreeRoot)
        unzipper = dir_packager.Unzipper(zipFilename=zipper.pkgFilename)
        unzipper.execute()
        self.verifyTree(self._contentTree)

    def tearDown(self):
        """Tear down the test fixture."""
        self._cleanFixtures()

    def _cleanFixtures(self):
        """Remove all test fixtures from the OS filesystem."""
        if (os.path.isdir(self._empty_dirname)):
            os.rmdir(self._empty_dirname)
        if (os.path.isfile(self._empty_zipname)):
            os.remove(self._empty_zipname)

        contentTreeZipName = '{0}.zip'.format(self._contentTreeRoot)
        if (os.path.isfile(contentTreeZipName)):
            os.remove(contentTreeZipName)
        if (os.path.isdir(self._contentTreeRoot)):
            shutil.rmtree(self._contentTreeRoot)

        emptyTreeZipName = '{0}.zip'.format(self._emptyTreeRoot)
        if (os.path.isfile(emptyTreeZipName)):
            os.remove(emptyTreeZipName)
        if (os.path.isdir(self._emptyTreeRoot)):
            shutil.rmtree(self._emptyTreeRoot)
        
    def makeTree(self, tree, root='.', content={}):
        """Creates a directory tree."""
        # make the root
        os.mkdir(root)
        # create the children of the root
        children = tree[os.path.basename(root)]
        for child in children:
            # if child is a directory
            if child in tree:
                self.makeTree(tree, os.path.join(root, child), content)
            # otherwise child is a file
            else:
                pathname = os.path.join(root, child)
                self.touchFile(pathname, content.get(child, ''))

    def touchFile(self, filename, content):
        """Creates an empty file named filename."""
        f = open(filename, 'w')
        f.write(content)
        f.close()

    def verifyTree(self, tree, root='', content={}):
        """Verify that the on-disk tree is the same as the tree."""
        if not os.path.exists(os.path.basename(root)):
            return False

        for child in tree[os.path.basename(root)]:
            pathname = os.path.join(root, child)
            if os.path.isfile(pathname):
                if not self.verifyContent(pathname, content[child]):
                    return False
            else:
                return self.verifyTree(tree,
                                       os.path.join(root, child),
                                       content)

        return True
    
            
def suite():
    """Returns the suite of unit tests in this module."""
    result = None
    return result


if __name__ == '__main__':
    unittest.main()
