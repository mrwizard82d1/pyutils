"""Remove the digit(s) version suffix from a set of filenames.

If a filename in the list has no digit version suffix, it is unchanged.
"""

import os
import re
import shutil
import sys


def remove_digit_version(filenames):
    for original in filenames:
        originalRoot, originalExt = os.path.splitext(original)
        unversionedRoot = re.sub(r'\d+$', '', originalRoot)
        renamed = unversionedRoot + originalExt
        shutil.move(original, renamed)


if __name__ == '__main__':
    remove_digit_version(sys.argv[1:])

    
        
