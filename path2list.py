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
                      help="Path to list (default = 'PATH')")
    (options, args) = parser.parse_args()
    if (len(args) > 0):
        print parser.print_help()
        sys.exit(1)

    thePath = os.environ[ options.path.upper() ]
    theListing = path2list( thePath )
    print theListing
    
