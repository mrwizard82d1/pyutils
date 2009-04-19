#! python


from optparse import OptionParser
import os


def dirname_to_svn_url(dirname):
    abs_dirname = os.path.abspath(dirname)
    drive, pathname = os.path.splitdrive(abs_dirname)
    result = "file:///{0}{1}".format(drive, pathname.replace("\\", "/"))
    return result


if __name__ == '__main__':
    usage = '%prog [options] dirname'
    parser = OptionParser()
    opts, args = parser.parse_args()
    svn_url = dirname_to_svn_url(args[0])
    print(svn_url)
    
