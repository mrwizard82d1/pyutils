#! env python


"""Archives a directory using the ZIP format."""


from optparse import OptionParser
import os

from dir_archive import ZipDirArchive


if __name__ == '__main__':
    usage = """%prog [options] dir_name

    Archive dir_name into a .zip file.
    """
    parser = OptionParser(usage=usage)
    parser.add_option('-z', '--zipname',
                      help="""Specify the .zip filename to be created.
                      If you do not supply a name, I will use a name
                      using the format <basename>.zip where <basename>
                      is the basename of the directory to be archived
                      and will place this file in the current directory.
                      """)

    opts, args = parser.parse_args()
    if len(args) != 1:
        parser.error("Exactly one dir_name required.")

    dirname = args[0]
    zipname = os.path.basename(dirname)
    zipper = ZipDirArchive(dirname, zipname)
    zipper.archive()
    
    
    
