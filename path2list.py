#! python


"""File to convert the output of PATH to a list."""


from optparse import OptionParser
import os
import sys


def path2list(thePath):
    """Converts a path listing to a whitespace separated list."""
    theItems = thePath.split( os.pathsep )
    theResult = '\n'.join( theItems )
    return theResult


if __name__ == '__main__':
    usage = "Usage: %prog [options]"
    parser = OptionParser(usage)
    parser.add_option('-p', '--path', dest='path', default='PATH',
                      help="Path to list (default = 'PATH' '-' for stdin)")
    (options, args) = parser.parse_args()
    if (len(args) > 0):
        parser.error('No arguments expected: {0}'.format(args))

    thePath = (os.environ[ options.path.upper() ] if
               options.path != '-' else
               sys.stdin.read())
    theListing = path2list( thePath )
    print(theListing)
    
