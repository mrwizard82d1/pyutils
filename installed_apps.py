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
    
    def find(self, filter='.*', what_info=[VERSION_KEY],
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

        what_info.append(NAME_KEY)
        all_installed = []
        for k in rd.keys():
            item = rd[k]

            info = {}
            for key in what_info:
                if key in rd[k]:
                    info[key] = item[key]

            all_installed.append(info)

        updates_pattern = re.compile('KB\d+')
        updates_installed = all_installed if \
                            include_updates else \
                            [info for info in all_installed if
                             NAME_KEY in info and
                             not updates_pattern.search(info[NAME_KEY])]

        filter_pattern = re.compile(filter, re.IGNORECASE)
        result = [info for info in updates_installed if
                  filter_pattern.search(info[NAME_KEY])]
        return result
    
