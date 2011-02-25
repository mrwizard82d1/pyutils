"""A directory walker.

This function is adapted from _Iron Python in Action_ by Michael Foord
and Christian Muirhead.
"""


import os


def walk(root, exclude_dirs):
    """Walk the directory tree root excluding the directories
    exclude_dirs.

    Note that this function is a generator yield each path
    representing a a file to the caller.
    """ 
    for entry in os.listdir(root):
        path = os.path.join(root, entry)
        if os.path.isfile(path):
            yield path
        elif os.path.isdir(path):
            if entry in exclude_dirs:
                continue

            # Recurse in all included sub-directories.
            for member in walk(path, exclude_dirs):
                yield member
                
