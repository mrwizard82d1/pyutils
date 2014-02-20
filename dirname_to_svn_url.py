#! env python


"""Script to convert a directory name to an SVN URL."""


from optparse import OptionParser
import os


def dirname_to_svn_url(dirname):
    abs_dirname = os.path.abspath(dirname)
    drive, pathname = os.path.splitdrive(abs_dirname)
    result = "file:///%s%s/" % (drive, pathname.replace("\\", "/"))
    return result


if __name__ == '__main__':
    usage = """%prog [options] dir_name

    Converts a directory name to an SVN URL.
    """
    parser = OptionParser(usage=usage)
    (opts, args) = parser.parse_args();
    if (len(args) != 1):
        parser.error("No dir_name supplied.");
        
    svn_url = dirname_to_svn_url(args[0])
    print(svn_url)
    
