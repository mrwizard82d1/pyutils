#! python


"""Command line script to manage mapped drives."""


from optparse import OptionParser

from mapped_drives import MappedDrives


def list_drives(md, options):
    for mapped_drive in md.drives():
        print('{0} -> {1}'.format(mapped_drive['local'], 
                                  mapped_drive['remote']))

def add_drive(md, options):
    options.__dict__['local'] = options.__dict__['drive']
    options.__dict__['remote'] = options.__dict__['share']
    del options.__dict__['drive']
    del options.__dict__['share']
    md.add(**options.__dict__)

def del_drive(md, options):
    md.delete(options.drive)

def reconnect_drives(md, options):
    md.reconnect()
    

actions = { 'list' : list_drives,
            'add' : add_drive,
            'del' : del_drive,
            'reconnect' : reconnect_drives }


if __name__ == '__main__':
    usage = """%prog [options] [command...]

    Managed mapped drives by applying commands. If no command is
    supplied, the script prints all mapped drives.

    Valid commands are:
    list\t- Print all mapped drives.
    add\t\t- Map the specified drive to the specified share.
    del\t\t- Remove the mapping of the specified drive.
    reconnect\t- Disconnects and reconnects all mapped drives.
    """
    parser = OptionParser(usage=usage)

    parser.add_option('-d', '--drive', default='W:',
                      help=('Drive letter of the mapped drive.' +
                            ' (default=W:)'))
    parser.add_option('-s', '--share',
                      default=r'\\jonesl-copiosae\c$',
                      help=('Share to be mapped' +
                            ' (default=\\jonesl-copiosae\c$).'))
    parser.add_option('-p', '--password',
                      help='Password for share.')
    parser.add_option('-u', '--username',
                      help='Resource username.')
    parser.add_option('-o', '--domainname',
                      help='Resource domainname.')

    (options, args) = parser.parse_args()
    if len(args) == 0:
        commands = ['list']
    else:
        commands = args

    md = MappedDrives()
    for command in commands:
        actions[command](md, options)
                      
                      
