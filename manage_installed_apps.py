#! python


"""Python script to list all installed software."""


from optparse import OptionParser
import pprint
import re

import win32con

from installed_apps import InstalledApps


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-t', '--text',
                      default='.*',
                      help='Select applications of interest (default=all).')
    (options, args) = parser.parse_args()
    
    ia = InstalledApps()
    installed = ia.find(filter=options.text)
    installed.sort()
    pprint.pprint(installed)
