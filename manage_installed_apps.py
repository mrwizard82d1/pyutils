#! python


"""Python script to list all installed software."""


from optparse import OptionParser
import pprint
import re
import subprocess

import win32con

from installed_apps import InstalledApps
from installed_apps import NAME_KEY
from installed_apps import UNINSTALL_KEY
from installed_apps import VERSION_KEY


class InstalledApp(object):
    """Models an installed application."""

    def __init__(self, name, version=None):
        """Initialize an instance with name and version."""
        self.name = name
        self.version = version

    def __lt__(self, other):
        """Am I less than other?"""
        if self.name < other.name:
            return True
        elif self.name > other.name:
            return False
        else:
            result = (self.version < other.version)
        
    def __str__(self):
        """Represent myself as a string."""
        return str((self.name, self.version))


def list_apps(ia, options):
    about_installed = ia.find(filter=options.text)
    installed = [InstalledApp(i['DisplayName'],
                              i.get('DisplayVersion')) for
                 i in about_installed]
    installed.sort()
    format_str = '{0:50.50}{1:25.25}'
    print(format_str.format('Name', 'Version'))
    print(format_str.format('=' * 48, '=' * 25))
    for i in installed:
        print(format_str.format(i.name, i.version))


def uninstall_apps(ia, options):
    to_uninstall = ia.find(filter=options.text,
                           what_info=[VERSION_KEY, UNINSTALL_KEY])
    for uninstall_info in to_uninstall:
        name = uninstall_info[NAME_KEY]
        version = uninstall_info[VERSION_KEY] if \
                  VERSION_KEY in uninstall_info else "N/A"
        uninstall_cmd = uninstall_info[UNINSTALL_KEY]
        prompt = 'Uninstall {0} (version {1}) (y/n)? '.format(name, version)
        answer = raw_input(prompt)
        if answer[0] in 'yY':
            subprocess.check_call(uninstall_cmd)


actions = { 'list' : list_apps,
            'uninstall' : uninstall_apps, }


if __name__ == '__main__':
    usage = """%prog [options] [command...]

    Manage installed applications. If no command is supplied, the
    script lists the installed applications.

    Valid commands are:
    list\t- Print the installed applications.
    uninstall\t- Uninstall the specified application(s).
    """
    parser = OptionParser(usage=usage)

    parser.add_option('-t', '--text',
                      default='.*',
                      help='Select applications of interest (default=all).')
    (options, args) = parser.parse_args()

    if len(args) == 0:
        commands = ['list']
    else:
        commands = args
    
    ia = InstalledApps()
    for command in commands:
        actions[command](ia, options)
