#!/usr/bin/env python
import os
import sys
import repl, interpreter, parser, compiler

def read_file(filename):
    fd = os.open(filename, os.O_RDONLY, 0777)
    contents = ''
    while True:
        buf = os.read(fd, 16)
        contents += buf
        if buf == '':
            return contents


def compile_file(filename):
    contents = read_file(filename)
    
    itpr = interpreter.Interpreter()
    ast = parser.parse(contents)
    bytecode = compiler.compile(ast)
    return itpr.interpret(bytecode).to_string()


def run(args):
    if len(args) == 1:
        compile_file(args[0])
        # print compile_file(args[0])
        
    elif len(args) == 0:
        repl.main()
    else:
        print "I don't understand these arguments"


if __name__ == '__main__':
    run(sys.argv[1:])
