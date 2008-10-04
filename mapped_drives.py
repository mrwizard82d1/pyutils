"""Manages mapped Windows drives."""


import wmi


NETWORK_DRIVE_TYPE = 4

class MappedDrives(object):

    def __init__(self):
        """MappedDrives() -> o."""
        self.c = wmi.WMI()
        
    def drives(self):
        """Returns a sequence of mapped drives."""
        result = [disk.Caption for disk in
                  self.c.Win32_LogicalDisk() if
                  disk.DriveType == NETWORK_DRIVE_TYPE]
        return result
    
