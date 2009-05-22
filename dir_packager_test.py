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
        
        
class PackageTest(object):
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

    def testArchiveEmptyDir(self):
        """Verify archiving and extracting an empty directory."""
        archive = self.toTest(self._empty_dirname)
        archive.archive()
        self.assertTrue(os.path.isfile(archive.pkgFilename))
        self.assertTrue(os.stat(archive.pkgFilename).st_size > 0)
        os.rmdir(self._empty_dirname)
        archive.extract()
        self.assertTrue(os.path.isdir(self._empty_dirname))
        self.assertTrue(len(os.listdir(self._empty_dirname)) == 0)

    def testArchiveEmptySubDirAmongFilesSkipsDir(self):
        """Archiving empty sub-directories among files skips empty
        directory but includes files.""" 
        archive = self.toTest(self._emptyTreeRoot)
        archive.archive()
        self.assertTrue(os.path.isfile(archive.pkgFilename))
        shutil.rmtree(self._emptyTreeRoot)
        archive.extract()
        self.verifyTree(self._emptyTree, self._emptyTreeRoot)

    def testArchiveSubdirZipsFileContent(self):
        """Verify that archiving a subdirectory includes file content."""
        archive = self.toTest(self._contentTreeRoot)
        archive.archive()
        self.assertTrue(os.path.isfile(archive.pkgFilename))
        shutil.rmtree(self._contentTreeRoot)
        archive.extract()
        self.verifyTree(self._contentTree, self._contentTreeRoot,
                        content=self._content)

    def testExtractIntoNewDirectoryHasCorrectTimes(self):
        """Extracing a archive into a new directory has correct times."""
        archive = self.toTest(self._contentTreeRoot)
        archive.archive()
        self.assertTrue(os.path.isfile(archive.pkgFilename))
        archive.extract(parentDirname=self._newDirname)
        self.assertTrue(os.path.isdir(self._newDirname))
        self.verifyTree(self._contentTree, self._contentTreeRoot,
                        content=self._content,
                        times=self._contentTimes)

    def testExtractHasCorrectTimeStamps(self):
        """Archive and extract a subdirectory restors time stamps."""
        archive = self.toTest(self._contentTreeRoot)
        archive.archive()
        self.assertTrue(os.path.isfile(archive.pkgFilename))
        shutil.rmtree(self._contentTreeRoot)
        archive.extract()
        self.verifyTree(self._contentTree, self._contentTreeRoot,
                        times=self._contentTimes)

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
    
    
class TgzArchiveTest(PackageTest, unittest.TestCase):
    """Defines the unit tests for the .tgz file packages."""

    def toTest(self, dirname=None, zipFilename=None):
        """Return the instance to test."""
        return dir_packager.TgzArchive(dirname, zipFilename)
    

class ZipPackageTest(PackageTest, unittest.TestCase):
    """Defines unit tests for the .zip file packages."""

    def toTest(self, dirname=None, zipFilename=None):
        """Return the instance to test."""
        return dir_packager.ZipPackager(dirname, zipFilename)
    
            
def suite():
    """Returns the suite of unit tests in this module."""
    result = None
    return result


if __name__ == '__main__':
    unittest.main()
