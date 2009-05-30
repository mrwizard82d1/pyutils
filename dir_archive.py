#! env python


"""Manages an archive in a particular format."""


from datetime import datetime
import os
import tarfile
import time
import zipfile


class Archive(object):
    """Common functions for all archives."""

    def __init__(self, dirname, archiveBase):
        """Archive(archiveBase) -> o

        Constructs an instance. If archiveBase is None, the archive
        base is dirname. If dirname is '/' (root) and archiveBase is
        None, the archiveBase is 'root'. If dirname is '.' (the
        current directory), raises ValueError.
        """
        
        if ((dirname == '.') or
            (dirname == os.getcwd())):
            raise ValueError('Directory cannot be' +
                             'current working directory.')
        
        self.dirname = dirname
        self._archiveBase = (archiveBase if 
                             archiveBase else
                             self.dirname)
        assert self._archiveBase, 'Archive base cannot be None.'

        if self.dirname == '/':
            self._archiveBase = 'root'

    def archiveFilename(self):
        """Returns the archive filename."""
        return self._archiveBase + self.archiveExt()


class TgzArchive(Archive):
    """Manages a .tgz archive."""

    EXT = '.tgz'
    
    def __init__(self, archiveBase, dirname=None):
        """TgzArchive(archiveBase, dirname=None) -> o

        Constructs an instance from a archiveBase. ArchiveBase is the
        archive filename without the extension. Note that dirname is
        only used by child classes.
        """
        super().__init__(dirname, archiveBase)

    def archiveExt(self):
        """Returns the format-specific extension.

        The returned value includes the leading dot ('.')
        """
        return TgzArchive.EXT
    
    def extract(self):
        tgzArchive = tarfile.open(self.archiveFilename(), 'r:*')
        try:
            tgzArchive.extractall()
        finally:
            tgzArchive.close()


class TgzDirArchive(TgzArchive):
    """Manages an .tgz (.tar.gz) archive of a directory."""

    def __init__(self, dirname, archiveBase=None):
        """TgzDirArchive(dirname, archiveBase=None) -> o

        Constructs an instance. If archiveBase is None, the archive
        base is dirname. 
        """
        super().__init__(archiveBase, dirname=dirname)

    def archive(self):
        """Archives my dirname into my archive filename."""
        tgzTarGzFilename = self.tarGzFilename()
        tgzArchive = tarfile.open(tgzTarGzFilename, 'w:gz')
        try:
            tgzArchive.add(self.dirname)
        finally:
            tgzArchive.close()
            
        if os.path.exists(self.archiveFilename()):
            os.remove(self.archiveFilename())
        os.rename(tgzTarGzFilename, self.archiveFilename())

    def tarGzFilename(self):
        """Returns my .tar.gz filename."""
        return self._archiveBase + '.tar.gz'


class ZipArchive(Archive):
    """Manages a .zip archive."""

    EXT = '.zip'
    
    def __init__(self, archiveBase, dirname=None):
        """ZipArchive(archiveBase, dirname=None) -> o

        Constructs an instance from archiveBase. ArchiveBase is the
        archive filename without the extension. Note that dirname is
        only used by child classes.
        """
        super().__init__(dirname, archiveBase)

    def archiveExt(self):
        """Returns the format-specific extension.

        The returned value includes the leading dot ('.')
        """
        return ZipArchive.EXT
    
    def extract(self):
        """Extract my archive into the current working directory."""
        zipFile = zipfile.ZipFile(self.archiveFilename(), 'r')
        try:
            infolist = zipFile.infolist()
            for member in infolist:
                if not self.isZippedDir(member):
                    zipFile.extract(member)
                else:
                    dirname = member.filename
                    os.mkdir(dirname)
                self.touch(member)
        finally:
            zipFile.close()

    def isZippedDir(self, member):
        """Determines if the member is a zipped (empty) directory."""
        result = False
        if ((member.filename[-1] == '/') and
            (member.external_attr == 48) and
            (member.file_size == 0)):
            result = True

        return result

    def touch(self, member):
        """Set the date and time of the extracted (already) member."""
        stat_time = self.zip_to_stat_time(member.date_time)
        os.utime(member.filename, (stat_time, stat_time))

    def zip_to_stat_time(self, zipTime):
        """Convert zipTime to a file 'stat' time."""
        # Convert zipTime (6-tuple) to datetime.
        date_time = datetime(*zipTime)

        # Convert datetime to tuple like time.localtime()
        time_tuple = date_time.timetuple()

        # Convert tuple to time integer.
        timeSeconds = time.mktime(time_tuple)

        # Return the integral seconds.
        return int(timeSeconds)
        

class ZipDirArchive(ZipArchive):
    """Manages an .zip (.tar.gz) archive of a directory."""

    def __init__(self, dirname, archiveBase=None):
        """ZipDirArchive(dirname, archiveBase=None) -> o

        Constructs an instance. If archiveBase is None, the archive
        base is dirname. 
        """
        super().__init__(archiveBase, dirname=dirname)

    def archive(self):
        """Archive the directory using the zip format."""
        zipFile = zipfile.ZipFile(self.archiveFilename(), 'w',
                                  zipfile.ZIP_DEFLATED)
        try:
            self.zip_tree(zipFile, self.dirname)
        finally:
            zipFile.close()

    def storeEmptyDir(self, zipFile, dirname):
        """Store the empty directory dirname."""
        dir_mtime = datetime.fromtimestamp(os.stat(dirname).st_mtime)
        zipTime = (dir_mtime.year, dir_mtime.month, dir_mtime.day,
                   dir_mtime.hour, dir_mtime.minute, dir_mtime.second)
        zipInfo = zipfile.ZipInfo(dirname + os.sep, zipTime)
        zipInfo.external_attr = 48
        zipFile.writestr(zipInfo, '')

    def zip_tree(self, zipFile, top):
        """Zip all files (recursively) beneath root into zipFile."""
        ## assert os.listdir(top), "Cannot zip empty root directory."
        for root, dirs, files in os.walk(top):
            # if the root directory contains something
            if (dirs or files):
                # zip all the files...
                for filename in files:
                    pathname = os.path.join(root, filename)
                    zipFile.write(pathname)
            # else the root directory is empty
            else:
                # store the empty directory
                self.storeEmptyDir(zipFile, root)
        


            
