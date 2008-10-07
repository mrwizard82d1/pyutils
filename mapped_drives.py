"""Manages mapped Windows drives."""


import win32net


class MappedDrives(object):

    def __init__(self):
        """MappedDrives() -> o."""
        
    def add(self, drive='W:', share='\\\\jonesl-copiosae\\c$'):
        """o.add(drive='W:', share=r'\\jonesl-copiosae\c$') -> None

        Adds a mapping between drive and share."""
        win32net.NetUseAdd(None, 1, {'local' : drive,
                                     'remote' : share})
        
    def delete(self, drive='W:'):
        """o.remove(drive='W:') -> None

        Removes any mapping for the specified drive."""
        win32net.NetUseDel(None, drive, 0)
        
    def drives(self):
        """Returns a sequence of mapped drives."""
        (mappings, total, handle) = win32net.NetUseEnum(None, 0)
        return [(mapping['local'], mapping['remote']) for
                mapping in mappings]

    def reconnect(self):
        """o.reconnect() -> None

        Disconnects and reconnects all mapped drives."""
        originals = self.drives()
        for drive, share in originals:
            self.delete(drive)

        for drive, share in originals:
            self.add(drive, share)

