#! env python


"""Defines and runs the unit tests for the dir_packager module."""


from datetime import datetime
import os
import shutil
import time
import unittest

import dir_archiver


class DirArchiveNameTest(unittest.TestCase):
    """Defines the name unit tests for the .zip file packagers."""

    def testDirnameNoPkgName(self):
        """Verify package name correct when dirname supplied."""
        toTest = dir_packager.ZipArchive('le_cheque')
        self.assertEqual('le_cheque', toTest.dirname)
        self.assertEqual('le_cheque.zip', toTest.pkgFilename)

    def testDirnamePkgName(self):
        """Verify the dirname and package name are both set correctly."""
        toTest = dir_packager.TgzArchive('ripis', 'olerinis.tgz', )
        self.assertEqual('olerinis.tgz', toTest.pkgFilename)
        self.assertEqual('ripis', toTest.dirname)

    def testNoDirnameNoPkgName(self):
        """Verify the dirname and package name when none are supplied."""
        toTest = dir_packager.TgzArchive()
        self.assertEqual('', toTest.dirname)
        self.assertEqual('dir_package.tgz', toTest.pkgFilename)

    def testNoDirnamePkgName(self):
        """Verify the dirname if only the package name if supplied."""
        filename = 'quaerunt.zip'
        toTest = dir_packager.ZipArchive(zipFilename=filename)
        self.assertEqual(os.path.splitext(filename)[0],
                         toTest.dirname)
        self.assertEqual(filename, toTest.pkgFilename)

    def testRootOnlyNoPkgname(self):
        """Verify the package name is correct if the dir is root."""
        toTest = dir_packager.ZipArchive('/')
        self.assertEqual('dir_package.zip', toTest.pkgFilename)
        self.assertEqual('/', toTest.dirname)
        
        
class ArchiveTest(object):
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
                           'reginae' : []}
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

    def assertContent(self, pathname, content):
        """Verify that the on-disk pathname has the correct content."""
        try:
            expected = content[os.path.basename(pathname)]
            actual = open(pathname, 'r').read()
            self.assertEqual(expected, actual,
                             'Cannot verify content of {0}.'.\
                             format(pathname))
        except KeyError:
            pass

    def assertTree(self, tree, root='', content={}, times={}):
        """Verify that the on-disk tree is the same as the tree."""
        self.assertTrue(os.path.exists(root),
                        'Root {0} does not exist.'.format(root))
        self.assertTime(root, times)

        for child in tree[os.path.basename(root)]:
            pathname = os.path.join(root, child)
            self.assertTime(pathname, times)

            if os.path.isfile(pathname):
                self.assertContent(pathname, content)
            else:
                return self.assertTree(tree,
                                       os.path.join(root, child),
                                       content)

    def assertTime(self, pathname, times):
        """Verify that the on-disk pathname has the correct time."""
        try:
            expectTimeStamp = times[os.path.basename(pathname)]
            expectTimeSeconds = time.mktime(datetime.\
                                            timetuple(expectTimeStamp))
            actualTimeSeconds = os.stat(pathname).st_mtime
            actualTimeStamp = datetime.fromtimestamp(actualTimeSeconds)
            msg = 'Restored time of {0}:\n  {1} != {2}.'.\
                  format(pathname, expectTimeStamp, actualTimeStamp)
            self.assertAlmostEqual(expectTimeSeconds,
                                   actualTimeSeconds,
                                   places=1,
                                   msg=msg)
        except KeyError:
            pass
    
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
            else :
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
        self.assertTree(self._emptyTree, self._emptyTreeRoot)

    def testArchiveSubdirZipsFileContent(self):
        """Verify that archiving a subdirectory includes file content."""
        archive = self.toTest(self._contentTreeRoot)
        archive.archive()
        self.assertTrue(os.path.isfile(archive.pkgFilename))
        shutil.rmtree(self._contentTreeRoot)
        archive.extract()
        self.assertTree(self._contentTree, self._contentTreeRoot,
                        content=self._content)

    def testExtractIntoNewDirectoryHasCorrectTimes(self):
        """Extracing a archive into a new directory has correct times."""
        archive = self.toTest(self._contentTreeRoot)
        archive.archive()
        self.assertTrue(os.path.isfile(archive.pkgFilename))
        archive.extract(parentDirname=self._newDirname)
        self.assertTrue(os.path.isdir(self._newDirname))
        self.assertTree(self._contentTree, self._contentTreeRoot,
                        content=self._content,
                        times=self._contentTimes)

    def testExtractHasCorrectTimeStamps(self):
        """Archive and extract a subdirectory restores time stamps."""
        archive = self.toTest(self._contentTreeRoot)
        archive.archive()
        self.assertTrue(os.path.isfile(archive.pkgFilename))
        shutil.rmtree(self._contentTreeRoot)
        archive.extract()
        self.assertTree(self._contentTree, self._contentTreeRoot,
                        times=self._contentTimes)

    def touchFile(self, pathname, times):
        """Set the access and modified times of pathname."""
        try:
            timeStamp = times[os.path.basename(pathname)]
            timeSeconds = time.mktime(datetime.timetuple(timeStamp))
            os.utime(pathname, (timeSeconds, timeSeconds))
        except KeyError:
            pass

    
class TgzArchiveTest(ArchiveTest, unittest.TestCase):
    """Defines the unit tests for the .tgz file packages."""

    def toTest(self, dirname=None, zipFilename=None):
        """Return the instance to test."""
        return dir_packager.TgzArchive(dirname, zipFilename)
    

class ZipArchiveTest(ArchiveTest, unittest.TestCase):
    """Defines unit tests for the .zip file packages."""

    def toTest(self, dirname=None, zipFilename=None):
        """Return the instance to test."""
        return dir_packager.ZipArchive(dirname, zipFilename)
    
            
def suite():
    """Returns the suite of unit tests in this module."""
    result = None
    return result


if __name__ == '__main__':
    unittest.main()
