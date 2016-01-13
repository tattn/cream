""" Execute ./cream <filename>
"""

import lexer, parser, interpreter, repl, cream
from rpython.jit.codewriter.policy import JitPolicy

def main(argv):
    cream.run(argv[1:])
    return 0

def target(driver, args):
    driver.exe_name = 'cream'
    return main, None

def jitpolicy(driver):
    return JitPolicy()
