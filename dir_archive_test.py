#! env python


"""Defines and runs the unit tests for the dir_archive module."""


from datetime import datetime
import os
import shutil
import time
import unittest

import dir_archive


class DirArchiveNameTest(unittest.TestCase):
    """Defines the name unit tests for the .zip file packagers."""

    def testCurrentWorkingDirectoryRaisesError(self):
        """Supplying the current working directory raises an error."""
        self.assertRaises(ValueError,
                          dir_archive.TgzDirArchive, '.', None)
        self.assertRaises(ValueError,
                          dir_archive.ZipDirArchive, os.getcwd(), None)
        
    def testDirnameNoPkgName(self):
        """Verify package name correct when dirname supplied."""
        toTest = dir_archive.ZipDirArchive('le_cheque')
        self.assertEqual('le_cheque', toTest.dirname)
        self.assertEqual('le_cheque.zip', toTest.archiveFilename())

    def testDirnamePkgName(self):
        """Verify the dirname and package name are both set correctly."""
        toTest = dir_archive.TgzDirArchive('ripis', 'olerinis', )
        self.assertEqual('olerinis.tgz', toTest.archiveFilename())
        self.assertEqual('ripis', toTest.dirname)

    def testNoDirnameNoPkgNameRaisesError(self):
        """Verify an error occurs if no archiveBase is supplied."""
        self.assertRaises(AssertionError, dir_archive.TgzArchive, None)

    def testNoDirnamePkgName(self):
        """Verify the dirname if only the package name if supplied."""
        filename = 'quaerunt'
        toTest = dir_archive.ZipArchive(archiveBase=filename)
        self.assertEqual(None, toTest.dirname)
        self.assertEqual(filename + toTest.archiveExt(),
                         toTest.archiveFilename())

    def testRootOnlyNoPkgname(self):
        """Verify the package name is correct if the dir is root."""
        toTest = dir_archive.ZipDirArchive('/')
        self.assertEqual('root.zip', toTest.archiveFilename())
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

    def _cleanFixtures(self):
        """Remove all test fixtures from the OS filesystem."""

        extensions = [dir_archive.TgzArchive.EXT,
                      dir_archive.ZipArchive.EXT]

        if (os.path.isdir(self._empty_dirname)):
            os.rmdir(self._empty_dirname)
        emptyArchiveNames = [(self._empty_dirname + ext) for
                             ext in extensions]
        for emptyArchiveName in emptyArchiveNames:
            if (os.path.isfile(emptyArchiveName)):
                os.remove(emptyArchiveName)

        if (os.path.isdir(self._contentTreeRoot)):
            shutil.rmtree(self._contentTreeRoot)
        contentTreeArchiveNames = [(self._contentTreeRoot + ext) for
                                   ext in extensions]
        for contentTreeArchiveName in contentTreeArchiveNames:
            if (os.path.isfile(contentTreeArchiveName)):
                os.remove(contentTreeArchiveName)

        emptyTreeZipName = '{0}.zip'.format(self._emptyTreeRoot)
        if (os.path.isdir(self._emptyTreeRoot)):
            shutil.rmtree(self._emptyTreeRoot)
        emptyTreeArchiveNames = [(self._emptyTreeRoot + ext) for
                                 ext in extensions]
        for emptyTreeArchiveName in emptyTreeArchiveNames:
            if (os.path.isfile(emptyTreeArchiveName)):
                os.remove(emptyTreeArchiveName)
        
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
            self.assertTrue(abs(expectTimeSeconds - actualTimeSeconds) <= 1,
                            msg)
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
        archive = self.toTestArchive(self._empty_dirname)
        archive.archive()
        self.assertTrue(os.path.isfile(archive.archiveFilename()))
        self.assertTrue(os.stat(archive.archiveFilename()).st_size > 0)
        os.rmdir(self._empty_dirname)
        extractor = self.toTestExtract(archive._archiveBase)
        extractor.extract()
        self.assertTrue(os.path.isdir(self._empty_dirname))
        self.assertTrue(len(os.listdir(self._empty_dirname)) == 0)

    def testArchiveEmptySubDirAmongFilesSkipsDir(self):
        """Archiving empty sub-directories among files skips empty
        directory but includes files."""
        archive = self.toTestArchive(self._emptyTreeRoot)
        archive.archive()
        self.assertTrue(os.path.isfile(archive.archiveFilename()))
        shutil.rmtree(self._emptyTreeRoot)
        extractor = self.toTestExtract(archive._archiveBase)
        extractor.extract()
        self.assertTree(self._emptyTree, self._emptyTreeRoot)

    def testArchiveSubdirZipsFileContent(self):
        """Verify that archiving a subdirectory includes file content."""
        archive = self.toTestArchive(self._contentTreeRoot)
        archive.archive()
        self.assertTrue(os.path.isfile(archive.archiveFilename()))
        shutil.rmtree(self._contentTreeRoot)
        extractor = self.toTestExtract(archive._archiveBase)
        extractor.extract()
        self.assertTree(self._contentTree, self._contentTreeRoot,
                        content=self._content)

    def testExtractHasCorrectTimeStamps(self):
        """Archive and extract a subdirectory restores time stamps."""
        archive = self.toTestArchive(self._contentTreeRoot)
        archive.archive()
        self.assertTrue(os.path.isfile(archive.archiveFilename()))
        shutil.rmtree(self._contentTreeRoot)
        extractor = self.toTestExtract(archive._archiveBase)
        extractor.extract()
        self.assertTree(self._contentTree, self._contentTreeRoot,
                        times=self._contentTimes)

    def tgzFilename(basename):
        """Return the .tgz filename corresponding to basename."""
        return basename + dir_archive.TgzArchive.EXT
    
    def touchFile(self, pathname, times):
        """Set the access and modified times of pathname."""
        try:
            timeStamp = times[os.path.basename(pathname)]
            timeSeconds = time.mktime(datetime.timetuple(timeStamp))
            os.utime(pathname, (timeSeconds, timeSeconds))
        except KeyError:
            pass

    def zipFilename(basename):
        """Return the .zip filename corresponding to basename."""
        return basename + dir_archive.ZipArchive.EXT
    
    
class TgzArchiveTest(ArchiveTest, unittest.TestCase):
    """Defines the unit tests for the .tgz file packages."""

    def toTestArchive(self, dirname=None, archiveBase=None):
        """Return the instance to archive."""
        return dir_archive.TgzDirArchive(dirname, archiveBase)

    def toTestExtract(self, archiveBase=None):
        """Return the instance from which to extract."""
        return dir_archive.TgzArchive(archiveBase)
    

class ZipArchiveTest(ArchiveTest, unittest.TestCase):
    """Defines unit tests for the .zip file packages."""

    def toTestArchive(self, dirname=None, archiveBase=None):
        """Return the instance to archive."""
        return dir_archive.ZipDirArchive(dirname, archiveBase)

    def toTestExtract(self, archiveBase=None):
        """Return the instance from which to extract."""
        return dir_archive.ZipArchive(archiveBase)
    
            
def suite():
    """Returns the suite of unit tests in this module."""
    suites = [
        unittest.TestLoader().loadTestsFromTestCase(DirArchiveNameTest),
        unittest.TestLoader().loadTestsFromTestCase(TgzArchiveTest),
        unittest.TestLoader().loadTestsFromTestCase(ZipArchiveTest),
        ]
    return unittest.TestSuite(suites)


if __name__ == '__main__':
    unittest.main()
