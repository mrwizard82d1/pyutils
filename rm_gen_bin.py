"""Utility to remove generated binary files from a directory."""


from __future__ import print_function
import argparse
import os
import re
import shutil


__author__ = 'ljones'


def print_rm_error_fn(is_verbose):

    def print_rm_error(function, path, exception_info):
        """Prints error information on attempted removal."""
        if not is_verbose:
            print('Error removing: {0}'.format(path))
        else:
            print('Error {0} removing {1} using {2}'.format(exception_info,
                                                            path, function))
    return print_rm_error

def rm_directory_if(starting_at, included_in, excluded_by, is_verbose):
    """Remove directories in start included_in but not excluded_by"""

    for root, directory_names, file_names in os.walk(starting_at):
        all_to_remove = set()
        all_to_skip = set()
        for directory_name in directory_names:
            # if directory_name by itself is to be excluded
            if any([exclude.search(directory_name) for exclude in
                    excluded_by]):
                # add it to the set to be skipped
                if is_verbose:
                    print('Skipping {0}.'.format(os.path.join(root,
                                                              directory_name)))
                all_to_skip.add(directory_name)

            # if directory_name is included but not excluded
            if any([include.search(directory_name) for include in
                    included_in]):
                if not any([exclude.search(os.path.join(root,
                                                        directory_name))
                            for exclude in excluded_by]):
                    all_to_remove.add(directory_name)

        # Remove matching directories
        for to_remove in all_to_remove:
            pathname = os.path.join(root, to_remove)
            if is_verbose:
                print('Removing {0}.'.format(pathname))
            shutil.rmtree(pathname, onerror=print_rm_error_fn(is_verbose))

        # Clean up the directories to be searched
        for to_remove in (all_to_remove | all_to_skip):
            del directory_names[directory_names.index(to_remove)]


if __name__ == '__main__':
    default_exclude = ['.hg', '.git']
    description = 'Remove generated directories matching a pattern' \
                  ' (skipping {0}).'.format(default_exclude)
    parser = argparse.ArgumentParser(description=description,
                                     formatter_class=
                                     argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--include', nargs='+', default=['bin', 'obj'],
                        help='Include pattern(s).')
    parser.add_argument('-x', '--exclude', nargs='+', default=[],
                        help='Exclude pattern(s).')
    parser.add_argument('-v', '--verbose', action='store_true',
                        default=False, help='Show verbose output.')
    parser.add_argument('where', nargs='*', default='.',
                        help='In directory')
    args = parser.parse_args()
    include_if = [re.compile(i) for i in args.include]
    exclude_if = [re.compile(x) for x in args.exclude] + \
                 [re.compile(default.replace('.', r'\.')) for default in
                  default_exclude]
    for start in args.where:
        rm_directory_if(start, include_if, exclude_if, args.verbose)

