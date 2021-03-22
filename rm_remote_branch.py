#! python

import argparse
import pathlib
import logging
import subprocess
import sys


def git_executable_path():
    result = pathlib.Path('C:/').joinpath('Program Files', 'Git', 'bin', 'git')
    return result

def create_local_rm_command(branch):
    result = f'{git_executable_path()} branch --delete {branch}'
    return result


def create_remote_rm_command(origin, branch):
    result = f'{git_executable_path()} push --delete {origin} {branch}'
    return result


def rm_branch(command):
    logging.info(f'Executing command, {command}.')
    retcode = subprocess.call(command)
    return retcode


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Remove local and remote branch.')
    parser.add_argument('branch', help='The branch to remove.')
    parser.add_argument('-o', '--origin', default='origin',
                        help='The remote from which to delete the branch. (Default: origin)')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Enable verbose output.')
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.INFO)


    try:
        rm_remote_branch_command = create_remote_rm_command(args.origin, args.branch)
        rm_remote_status = rm_branch(rm_remote_branch_command)
        if rm_remote_status != 0:
            print(f'Command, "{rm_remote_branch_command}", failed: {rm_remote_status}', file=sys.stderr)
            sys.exit(rm_remote_status)
    except OSError as oe:
        print(f'Execution of command, "{rm_remote_branch_command}", failed: {oe}', file=sys.stderr)

    try:
        rm_local_branch_command = create_local_rm_command(args.branch)
        rm_local_status = rm_branch(rm_local_branch_command)
        if rm_local_status != 0:
            print(f'Command, "{rm_local_branch_command}", failed: {rm_local_status}', file=sys.stderr)
            sys.exit(rm_local_status)
    except OSError as oe:
        print(f'Execution of command, "{rm_local_branch_command}", failed: {oe}', file=sys.stderr)

