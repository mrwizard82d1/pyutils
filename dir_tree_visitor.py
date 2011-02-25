"""Defines a function to visit every node in a specified directory tree."""


import os


def dir_visitor(root, visitor):
    """Applies the function visitor to each node in the directory tree
    root.

    The visitor is a function accepting three arguments. The first
    argument is the pathname identifying the directory the visitor is
    currently processing. The second argument is a list containing all
    directories in the directory being processed by the visitor. The
    third argument is a list of files in the directory being
    processed. For convenience, this module also includes a visitor
    'wrapper' that only invokes a visitor function accepting a single
    argument: the pathname of the file being visited."""

    for root_pathname, dirs, files in os.walk(root):
        visitor(root_pathname, dirs, files)


class SimpleVisitor(object):
    """A simple visitor wrapping a callable expecting the pathname of
    files to visit."""
    
    def __init(callable):
        """SimpleVisitor(callable) -> o

        Initialize an instance with the specified callable."""
        
        self._simple_visitor = callable

    def __call__(root_pathname, dirs, files):
        """Invokes this visitor passing the root pathname, the list of
        directories in that root, and the list of files in that
        root."""

        for file in files:
            file_pathname = os.path.join(root_pathname, file)
            self._simple_visitor(file_pathname)

