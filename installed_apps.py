#! python


"""Models installed applications."""


import os
import re

import win32con

import reg_dict


NAME_KEY='DisplayName'
VERSION_KEY='DisplayVersion'
UNINSTALL_KEY='UninstallString'


class InstalledApps(object):
    """Models the installed applications."""
    
    def find(filter='.*', what_info=[VERSION_KEY],
             include_updates=False):
        """o.find(filter, what_info, include_updates) -> seq

        Finds all installed applications matching filter.

        filter - Regular expression to match (default='.*').
        what_info - Information to return (default='DisplayVersion').
        Note that the list always includes 'DisplayName' if available. 
        include_updates - Flag if result includes Windows updates
        (default=False)."""
        
        # Create a registry dictionary to query.
        keypath = os.path.join('Software', 'Microsoft', 'Windows',
                               'CurrentVersion', 'Uninstall')
        rd = reg_dict.RegistryDict(keypath=keypath,
                                   flags=win32con.KEY_ALL_ACCESS)

        what_info.append[NAME_KEY]
        raw_result = []
        for k in rd.keys():
            item = rd[k]

            info = {}
            for key in what_info:
                if key in rd[k]:
                    info[key] = item[key]

            raw_result.append(info)

        updates_result = raw_result
        if not include_updates :
            regexp = re.compile('KB\d+')
            update_result = [info for info in raw_result if
                             not regexp.search(info[NAME_KEY])]

        regexp = re.compile(filter, re.IGNORECASE)
        result = [info for info in updates_result if
                  regexp.search(info[NAME_KEY])]
        return result
    
