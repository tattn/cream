#!/usr/bin/env python
import sys
import shlex, subprocess

if __name__ == "__main__":
    argv = sys.argv
    if len(argv) == 0:
        command = shlex.split("%s %s --output %s %s" % (PYTHON, RPYTHON, BINARY, TARGET))
        p = subprocess.Popen(command)
    elif argv[1] == 'run':
        command = "PYTHONPATH=../pypy-4.0.1 python cream.py examples/fact.bd"
        print(command)
        subprocess.call(command, shell=True)
        
