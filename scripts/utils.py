from subprocess import call
import os
def run(command):
    print("Running: ", command)
    os.system(command)
