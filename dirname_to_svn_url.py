#! /cygdrive/c/Python25/python.exe


import sys
import os


def dirname_to_svn_url(dirname):
    abs_dirname = os.path.abspath(dirname)
    drive, pathname = os.path.splitdrive(abs_dirname)
    result = "file:///%s%s/" % (drive, pathname.replace("\\", "/"))
    return result


if __name__ == '__main__':
    svn_url = dirname_to_svn_url(sys.argv[1])
    print svn_url
    
