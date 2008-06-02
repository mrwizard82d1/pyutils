"""Convert the extensions of a set of supplied filenames to lower case.

If the extension is already lowercase, this function does nothing.
"""

import os
import shutil
import sys


def downcase_ext(filenames):
    for original in filenames:
        originalRoot, originalExt = os.path.splitext(original)
        lowerCaseExt = originalExt.lower()
        renamed = originalRoot + lowerCaseExt
        shutil.move(original, renamed)


if __name__ == '__main__':
    downcase_ext(sys.argv[1:])

    
        
