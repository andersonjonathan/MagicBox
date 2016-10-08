from subprocess import call


def set_volume(left, right=None):
    if right is None:
        right = left
    call(["amixer", "-D", "pulse", "sset", "Master", "{}%,{}%".format(left, right)])
