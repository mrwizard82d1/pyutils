#! env python


"""Manages packaging directories into single files."""


from datetime import datetime
import os
import zipfile


class Packager(object):
    """Provides common services for all child classes."""

    def __init__(self, dirname=None, pkgFilename=None):
        """Instance for recursively packaging dirname into pkgFilename. 

        If dirname is not supplied, I package the current working
        directory. If pkgFilename is not supplied, I construct one
        from dirname. If dirname is '' (the default), pkgFilename is
        the current working directory name with .zip
        appended. Otherwise, it is the basename of the specified
        directory with .zip appended.
        """
        if not dirname and not pkgFilename:
            self.dirname = ''
            self.pkgFilename = 'dir_package.zip'
        elif dirname and not pkgFilename:
            self.dirname = dirname
            head, tail = os.path.split(self.dirname)
            while head != '/' and not tail:
                head, tail = os.path.split(self.dirname)
            basename = (tail if tail else 'dir_package')
            self.pkgFilename = '{0}.zip'.format(basename)
        elif not dirname and pkgFilename:
            self.dirname = os.path.splitext(pkgFilename)[0]
            self.pkgFilename = pkgFilename
        else:
            # both dirname and pkgFilename
            self.dirname = dirname
            self.pkgFilename = pkgFilename

    def execute(self):
        raise NotImplementedError('{0}.execute() not implemented.'.
                                  format(self.__class__.__name__))


class Zipper(Packager):
    """Models a command to create a .zip file from a directory."""

    def __init__(self, dirname=None, zipFilename=None):
        """Instance for recursively packaging dirname into zipFilename."""
        super(Zipper, self).__init__(dirname, zipFilename)

    def execute(self):
        """Zip the directory into the zip filename."""
        zipFile = zipfile.ZipFile(self.pkgFilename, 'w')
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
                # zip all the directories...
                for dirname in dirs:
                    pathname = os.path.join(root, dirname)
                    self.zip_tree(zipFile, pathname)
            # else the root directory is empty
            else:
                # store the empty directory
                self.storeEmptyDir(zipFile, root)
        

class Unzipper(Packager):
    """Models a command to extract all files from a .zip file."""

    def __init__(self, dirname=None, zipFilename=None):
        """Instance for recursively packaging dirname into zipFilename."""
        super(Unzipper, self).__init__(dirname, zipFilename)

    def execute(self):
        """Unzip the zip filename into directory."""
        zipFile = zipfile.ZipFile(self.pkgFilename, 'r')
        try:
            infolist = zipFile.infolist()
            for member in infolist:
                if not self.isZippedDir(member):
                    zipFile.extract(member)
                else:
                    dirname = member.filename
                    os.mkdir(dirname)
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
                
