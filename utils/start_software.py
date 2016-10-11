import os
from subprocess import call, STDOUT
from threading import Thread

FNULL = open(os.devnull, 'w')


def start_software(*args):
    thread = Thread(target=call, args=args, kwargs={'stdout': FNULL, 'stderr': STDOUT})
    thread.start()
