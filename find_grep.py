"""Executes grep within a 'find' command."""


import fnmatch
from optparse import OptionParser
import os
import re


def find_grep(start, file_name_pattern, content_pattern):
    filenames_of_interest = []
    content_matcher = re.compile(content_pattern, re.IGNORECASE)
    for root, dirs, files in os.walk(start):
        matching_files = fnmatch.filter(files, file_name_pattern)
        for matching_file in matching_files:
            filename_of_interest = os.path.join(root, matching_file)
            contents = open(filename_of_interest).read()
            if content_matcher.search(contents):
                filenames_of_interest.append(filename_of_interest)
    return filenames_of_interest


if __name__ == '__main__':
    usage = """
    %prog [options] [dir_name (default current)]

    Find all matching files containing a pattern within a directory.
    """
    parser = OptionParser(usage)
    parser.add_option('-f', '--file_pattern', default='*',
                      help='Pattern of filenames to search (default=all).')
    parser.add_option('-t', '--text_pattern', default='.',
                      help='Pattern of content to match (default=any).')
    parser.add_option('-d', '--display_cmd_line', default=False,
                      action='store_true',
                      help=('Display the original command line' +
                            ' (used for diagnosing' +
                            ' shell expansion issues).'))
    options, args = parser.parse_args()

    if options.display_cmd_line:
        import sys
        print('sys.argv={0}'.format(sys.argv))

    if len(args) == 0:
        start_dirname = '.'
    elif len(args) == 1:
        start_dirname = args[0]
    elif len(args) > 1:
        parser.error("Too many directories.")

    matching_filenames = find_grep(start_dirname, options.file_pattern,
                                   options.text_pattern)
    matching_filenames.sort()
    for matching_filename in matching_filenames:
        print(matching_filename)

    
