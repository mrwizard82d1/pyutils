#! env python


"""Defines and runs the unit tests for the dir_packager module."""


from datetime import datetime
import os
import shutil
import time
import unittest

import dir_packager


class DirPackagerNameTest(unittest.TestCase):
    """Defines the name unit tests for the .zip file packagers."""

    def testDirnameNoPkgName(self):
        """Verify package name correct when dirname supplied."""
        zipPackager = dir_packager.ZipPackager('le_cheque')
        self.assertEqual('le_cheque', zipPackager.dirname)
        self.assertEqual('le_cheque.zip', zipPackager.pkgFilename)

    def testDirnamePkgName(self):
        """Verify the dirname and package name are both set correctly."""
        zipPackager = dir_packager.ZipPackager('ripis', 'olerinis.zip', )
        self.assertEqual('olerinis.zip', zipPackager.pkgFilename)
        self.assertEqual('ripis', zipPackager.dirname)

    def testNoDirnameNoPkgName(self):
        """Verify the dirname and package name when none are supplied."""
        zipPackager = dir_packager.ZipPackager()
        self.assertEqual('', zipPackager.dirname)
        self.assertEqual('dir_package.zip', zipPackager.pkgFilename)

    def testNoDirnamePkgName(self):
        """Verify the dirname if only the package name if supplied."""
        filename = 'quaerunt.zip'
        zipPackager = dir_packager.ZipPackager(zipFilename=filename)
        self.assertEqual(os.path.splitext(filename)[0],
                         zipPackager.dirname)
        self.assertEqual(filename, zipPackager.pkgFilename)

    def testRootOnlyNoPkgname(self):
        """Verify the package name is correct if the dir is root."""
        zipPackager = dir_packager.ZipPackager('/')
        self.assertEqual('dir_package.zip', zipPackager.pkgFilename)
        self.assertEqual('/', zipPackager.dirname)
        
        
class PackageTest(unittest.TestCase):
    """Defines the common set up and tear down for package tests."""

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
        self._contentTimes = {'scirit' : datetime(1995, 12, 5, 8, 56, 3)}
        self._empty_dirname = 'nulla'
        self._empty_zipname = '{0}.zip'.format(self._empty_dirname)
        self._emptyTree = {'necessaire' : ['aqua', 'voluisti',
                                           'reginae', 'invetavi'],
                           'reginiae' : []}
        self._emptyTreeRoot = 'necessaire'

        self._newDirname = 'venatibus'

        # clean old fixtures
        self._cleanFixtures()
        
        # set up new fixtures
        os.mkdir(self._empty_dirname)
        self.makeTree(self._emptyTree, self._emptyTreeRoot)
        self.makeTree(self._contentTree, self._contentTreeRoot,
                      content=self._content, times=self._contentTimes)

    def tearDown(self):
        """Tear down the test fixture."""
        self._cleanFixtures()
        pass

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
        
        if os.path.exists(self._newDirname):
            shutil.rmtree(self._newDirname)

    def makeFile(self, filename, content):
        """Creates an empty file named filename."""
        f = open(filename, 'w')
        f.write(content)
        f.close()

    def makeTree(self, tree, root='.', content={}, times={}):
        """Creates a directory tree."""
        # make the root
        os.mkdir(root)
        self.touchFile(root, times)
        # create the children of the root
        children = tree[os.path.basename(root)]
        for child in children:
            # if child is a directory
            if child in tree:
                self.makeTree(tree, os.path.join(root, child), content)
            # otherwise child is a file
            else:
                pathname = os.path.join(root, child)
                self.makeFile(pathname, content.get(child, ''))
                self.touchFile(pathname, times)

    def touchFile(self, pathname, times):
        """Set the access and modified times of pathname."""
        try:
            timeStamp = times[os.path.basename(pathname)]
            timeSeconds = time.mktime(datetime.timetuple(timeStamp))
            os.utime(pathname, (timeSeconds, timeSeconds))
        except KeyError:
            pass

    def verifyContent(self, pathname, content):
        """Verify that the on-disk pathname has the correct content."""
        try:
            expected = content[os.path.basename(pathname)]
            actual = open(pathname, 'r').read()
            return (expected == actual)
        except KeyError:
            return True

    def verifyTree(self, tree, root='', content={}, times={}):
        """Verify that the on-disk tree is the same as the tree."""
        if not os.path.exists(root):
            return False
        if not self.verifyTime(root, times):
            return False

        for child in tree[os.path.basename(root)]:
            pathname = os.path.join(root, child)
            if not self.verifyTime(pathname, times):
                return False
            if os.path.isfile(pathname):
                if not self.verifyContent(pathname, content):
                    return False
            else:
                return self.verifyTree(tree,
                                       os.path.join(root, child),
                                       content)

        return True

    def verifyTime(self, pathname, times):
        """Verify that the on-disk pathname has the correct time."""
        try:
            timeStamp = times[os.path.basename(pathname)]
            timeSeconds = time.mktime(datetime.timetuple(timeStamp))
            return (timeSeconds == os.stat(pathname).st_mtime)
        except KeyError:
            return True
    
    
class TgzPackageTest(unittest.TestCase):
    """Defines the unit tests for the .tgz file packages."""
    pass


class ZipPackageTest(PackageTest):
    """Defines unit tests for the .zip file packages."""

    def testUnzipIntoNewDirectoryHasCorrectTimes(self):
        """Unzipping a package into a new directory has correct times."""
        zipPackager = dir_packager.ZipPackager(self._contentTreeRoot)
        zipPackager.archive()
        zipPackager.extract(parentDirname=self._newDirname)
        self.assertTrue(os.path.isdir(self._newDirname))
        self.verifyTree(self._contentTree, self._contentTreeRoot,
                        content=self._content,
                        times=self._contentTimes)

    def testUnzipHasCorrectTimeStamps(self):
        """Verify that unzipping a subdirectory restores time stamps."""
        zipPackager = dir_packager.ZipPackager(self._contentTreeRoot)
        zipPackager.archive()
        shutil.rmtree(self._contentTreeRoot)
        zipPackager.extract()
        self.verifyTree(self._contentTree, self._contentTreeRoot,
                        times=self._contentTimes)

    def testZipEmptyDir(self):
        """Verify zipping an empty directory."""
        zipPackager = dir_packager.ZipPackager(self._empty_dirname)
        zipPackager.archive()
        self.assertTrue(os.path.isfile(zipPackager.pkgFilename))
        self.assertTrue(os.stat(zipPackager.pkgFilename).st_size > 0)
        os.rmdir(self._empty_dirname)
        zipPackager.extract()
        self.assertTrue(os.path.isdir(self._empty_dirname))
        self.assertTrue(len(os.listdir(self._empty_dirname)) == 0)

    def testZipEmptySubDirAmongFilesSkipsDir(self):
        """Verify that zipPackager skips empty directory but zips files."""
        zipPackager = dir_packager.ZipPackager(self._emptyTreeRoot)
        zipPackager.archive()
        shutil.rmtree(self._emptyTreeRoot)
        zipPackager.extract()
        self.verifyTree(self._emptyTree, self._emptyTreeRoot)

    def testZipSubdirZipsFileContent(self):
        """Verify that zipping a subdirectory zips file content."""
        zipPackager = dir_packager.ZipPackager(self._contentTreeRoot)
        zipPackager.archive()
        shutil.rmtree(self._contentTreeRoot)
        zipPackager.extract()
        self.verifyTree(self._contentTree, self._contentTreeRoot,
                        content=self._content)

            
def suite():
    """Returns the suite of unit tests in this module."""
    result = None
    return result


if __name__ == '__main__':
    unittest.main()
