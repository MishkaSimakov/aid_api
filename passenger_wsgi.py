import sys
import os

INTERP = os.path.expanduser("/var/www/u2552113/data/aid/bin/python")
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.append(os.getcwd())

from server import application
