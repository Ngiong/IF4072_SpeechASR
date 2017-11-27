from subprocess import call
import os
import sys
def run(command):
    print("Running: ", command)
    status = os.system(command)
    if (status != 0):
        sys.exit()
