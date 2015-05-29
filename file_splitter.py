from subprocess import call
import sys

argv = sys.argv


call(["split", "-b", "4096", argv[0], "output"])

