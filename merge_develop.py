#! python

import sys
import subprocess

def merge_develop_into(target):
    subprocess.run('git co %s' % target)
    subprocess.run('git merge develop')
    subprocess.run('git st')
    subprocess.run('git push')

if (__name__ == '__main__'):
    for branch in sys.argv[1:]:
        merge_develop_into(branch)
