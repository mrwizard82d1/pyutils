#! python


"""Python script to list all installed software."""


from optparse import OptionParser
import pprint
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
        
        display_name = ''
        if 'DisplayName' in rd[k]:
            display_name = item['DisplayName']
            
        display_version = ''
        if 'DisplayVersion' in rd[k]:
            display_version = item['DisplayVersion']
            
        raw_result.append((display_name, display_version))
    
    updates_result = raw_result
    if not include_updates:
        regexp = re.compile('KB\d+')
        updates_result = [(name, version) for name, version in
                          raw_result if not regexp.search(name)]
      
    regexp = re.compile(filter, re.IGNORECASE)
    result = [(name, version) for name, version in updates_result if
              regexp.search(name)]
    return result


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-t', '--text',
                      default='.*',
                      help='Select applications of interest (default=all).')
    (options, args) = parser.parse_args()
    
    installed = query_uninstallable(filter=options.text)
    installed.sort()
    pprint.pprint(installed)
