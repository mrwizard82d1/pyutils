"""Manages mapped Windows drives."""


import win32net


class MappedDrives(object):

    def __init__(self):
        """MappedDrives() -> o."""
        
    def add(self, **kwargs):
        """o.add(**kwargs) -> None

        Adds a mapping between drive (local) and share (remote).

        The required keyword arguments are local (drive) and remote
        (share). The optional keyword arguments are password, username
        and domainname. 
        """
        args = {'local': 'W:', 'share': '\\jonesl-copiosae\c$',
                'password': None, 'username': None,
                'domainname': None}
        args.update(kwargs)
        if 'password' not in args:
            win32net.NetUseAdd(None, 0, kwargs)
        elif (('username' not in args)and
              ('domainname' not in args)):
            win32net.NetUseAdd(None, 1, kwargs)
        else:
            win32net.NetUseAdd(None, 2, kwargs)
        
    def delete(self, drive='W:'):
        """o.remove(drive='W:') -> None

        Removes any mapping for the specified drive."""
        win32net.NetUseDel(None, drive, 0)
        
    def drives(self):
        """Returns a sequence of mapped drives."""
        (mapped_drives, total, handle) = win32net.NetUseEnum(None, 0)
        return mapped_drives

    def reconnect(self):
        """o.reconnect() -> None

        Disconnects and reconnects all mapped drives."""
        mapped_drives = self.drives()
        for mapped_drive in mapped_drives:
            self.delete(mapped_drive['drive'])

        for mapped_drive in mapped_drives:
            self.add(mapped_drive)

