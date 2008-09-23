"""Python script to list all installed software."""


from optparse import OptionParser
import re

import win32con

import reg_dict


def query_uninstallable(filter='.*', include_updates=False):
    # Create a registry dictionary to query.
    keypath = 'Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\'
    rd = reg_dict.RegistryDict(keypath=keypath,
                               flags=win32con.KEY_ALL_ACCESS)
    raw_result = []
    for k in rd.keys():
        item = rd[k]
        if 'DisplayName' in rd[k]:
            raw_result.append(item['DisplayName'])
    
    updates_result = raw_result
    if not include_updates:
      regexp = re.compile('KB\d+')
      updates_result = [n for n in raw_result if not regexp.search(n)]
      
    regexp = re.compile(filter)
    result = [n for n in updates_result if regexp.search(n)]
    return result

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-t', '--text',
                      default='.*',
                      help='Select applications of interest (default=all).')
    (options, args) = parser.parse_args()
    
    names = query_uninstallable(filter=options.text)
    names.sort()
    print names
    
