#! env python


"""Manages an archive in a particular format."""


from datetime import datetime
import os
import tarfile
import time
import zipfile


class Archive(object):
    """Common functions for all archives."""

    def __init__(self, dir_name, archive_base):
        """Archive(dir_name, archive_base) -> o

        Constructs an instance. If archive_base is None, the archive
        base is dir_name. If dir_name is '/' (root) and archive_base is
        None, the archive_base is 'root'. If dir_name is '.' (the current
        directory), raises ValueError."""
        
        if (dir_name == '.') or (dir_name == os.getcwd()):
            raise ValueError('Directory cannot be' +
                             'current working directory.')
        
        self.dir_name = dir_name
        self._archive_base = (archive_base if
                              archive_base else
                              self.dir_name)
        assert self._archive_base, 'Archive base cannot be None.'

        if self.dir_name == '/':
            self._archive_base = 'root'

    def archive_ext(self):
        raise NotImplementedError

    def archive_filename(self):
        """Returns the archive filename."""
        return self._archive_base + self.archive_ext()


class TgzArchive(Archive):
    """Manages a .tgz archive."""

    EXT = '.tgz'
    
    def __init__(self, archive_base, dir_name=None):
        """TgzArchive(archive_base, dir_name=None) -> o

        Constructs an instance from a archive_base. ArchiveBase is the
        archive filename without the extension. Note that dir_name is
        only used by child classes.
        """
        super(TgzArchive, self).__init__(dir_name, archive_base)

    def archive_ext(self):
        """Returns the format-specific extension.

        The returned value includes the leading dot ('.')
        """
        return TgzArchive.EXT
    
    def extract(self):
        tgz_archive = tarfile.open(self.archive_filename(), 'r:*')
        try:
            tgz_archive.extractall()
        finally:
            tgz_archive.close()


class TgzDirArchive(TgzArchive):
    """Manages an .tgz (.tar.gz) archive of a directory."""

    def __init__(self, dir_name, archive_base=None):
        """TgzDirArchive(dir_name, archive_base=None) -> o

        Constructs an instance. If archive_base is None, the archive
        base is dir_name.
        """
        super(TgzDirArchive, self).__init__(archive_base, dir_name=dir_name)

    def archive(self):
        """Archives my dir_name into my archive filename."""
        tgz_tar_gz_filename = self.tar_gz_filename()
        tgz_archive = tarfile.open(tgz_tar_gz_filename, 'w:gz')
        try:
            tgz_archive.add(self.dir_name)
        finally:
            tgz_archive.close()
            
        if os.path.exists(self.archive_filename()):
            os.remove(self.archive_filename())
        os.rename(tgz_tar_gz_filename, self.archive_filename())

    def tar_gz_filename(self):
        """Returns my .tar.gz filename."""
        return self._archive_base + '.tar.gz'


class ZipArchive(Archive):
    """Manages a .zip archive."""

    EXT = '.zip'
    
    def __init__(self, archive_base, dir_name=None):
        """ZipArchive(archive_base, dir_name=None) -> o

        Constructs an instance from archive_base. ArchiveBase is the
        archive filename without the extension. Note that dir_name is
        only used by child classes.
        """
        super(ZipArchive, self).__init__(dir_name, archive_base)

    def archive_ext(self):
        """Returns the format-specific extension.

        The returned value includes the leading dot ('.')
        """
        return ZipArchive.EXT
    
    def extract(self):
        """Extract my archive into the current working directory."""
        zip_file = zipfile.ZipFile(self.archive_filename(), 'r')
        try:
            infolist = zip_file.infolist()
            for member in infolist:
                if not self.is_zipped_dir(member):
                    zip_file.extract(member)
                else:
                    dir_name = member.filename
                    os.mkdir(dir_name)
                self.touch(member)
        finally:
            zip_file.close()

    def is_zipped_dir(self, member):
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

    def zip_to_stat_time(self, zip_time):
        """Convert zip_time to a file 'stat' time."""
        # Convert zip_time (6-tuple) to datetime.
        date_time = datetime(*zip_time)

        # Convert datetime to tuple like time.localtime()
        time_tuple = date_time.timetuple()

        # Convert tuple to time integer.
        time_seconds = time.mktime(time_tuple)

        # Return the integral seconds.
        return int(time_seconds)
        

class ZipDirArchive(ZipArchive):
    """Manages an .zip (.tar.gz) archive of a directory."""

    def __init__(self, dir_name, archive_base=None):
        """ZipDirArchive(dir_name, archive_base=None) -> o

        Constructs an instance. If archive_base is None, the archive
        base is dir_name.
        """
        super(ZipDirArchive, self).__init__(archive_base, dir_name=dir_name)

    def archive(self):
        """Archive the directory using the zip format."""
        zip_file = zipfile.ZipFile(self.archive_filename(), 'w',
                                   zipfile.ZIP_DEFLATED)
        try:
            self.zip_tree(zip_file, self.dir_name)
        finally:
            zip_file.close()

    def store_empty_dir(self, zip_file, dir_name):
        """Store the empty directory dir_name."""
        dir_modified_time = datetime.fromtimestamp(os.stat(dir_name).st_mtime)
        zip_time = (dir_modified_time.year, dir_modified_time.month,
                    dir_modified_time.day, dir_modified_time.hour,
                    dir_modified_time.minute, dir_modified_time.second)
        zip_info = zipfile.ZipInfo(dir_name + os.sep, zip_time)
        zip_info.external_attr = 48
        zip_file.writestr(zip_info, '')

    def zip_tree(self, zip_file, top):
        """Zip all files (recursively) beneath root into zip_file."""
        ## assert os.listdir(top), "Cannot zip empty root directory."
        for root, dirs, files in os.walk(top):
            # if the root directory contains something
            if dirs or files:
                # zip all the files...
                for filename in files:
                    pathname = os.path.join(root, filename)
                    zip_file.write(pathname)
            # else the root directory is empty
            else:
                # store the empty directory
                self.store_empty_dir(zip_file, root)
        

