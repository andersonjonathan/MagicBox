import os
from subprocess import call, STDOUT

FNULL = open(os.devnull, 'w')


def set_volume(left, right=None):
    if right is None:
        right = left
    call(["amixer", "-D", "pulse", "sset", "Master", "{}%,{}%".format(left, right)], stdout=FNULL, stderr=STDOUT)
