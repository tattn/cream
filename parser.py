from rply import ParserGenerator
from rply.token import BaseBox, Token
from ast import *
from errors import *
import lexer
import os

TAB_WIDTH = 4

class ParserState(object):
    def __init__(self):
        self.indent = 0
        # declared variables
        self.variables = {}

pg = ParserGenerator(
    # All token names
    ['STRING', 'INTEGER', 'FLOAT', 'IDENTIFIER', 'BOOLEAN',
     'PLUS', 'MINUS', 'MUL', 'DIV',
     'IF', 'ELSE', 'COLON', 'END', 'AND', 'OR', 'NOT', 'WHILE',
     '(', ')', 'PARENCOLON', '=', '==', '!=', '>=', '<=', '<', '>', '[', ']', ',',
     '{','}',
     '$end', 'NEWLINE', 'FUNCTION', 'INDENT',
    ],
    # Precedence rules
    precedence = [
        ('left', ['FUNCTION',]),
        # ('left', ['LET',]),
        ('left', ['=']),
        ('left', ['[', ']', ',',]),
        ('left', ['IF', 'COLON', 'ELSE', 'END', 'NEWLINE','WHILE',]),
        ('left', ['PARENCOLON']),
        ('left', ['AND', 'OR',]),
        ('left', ['NOT',]),
        ('left', ['==', '!=', '>=','>', '<', '<=',]),
        ('left', ['PLUS', 'MINUS',]),
        ('left', ['MUL', 'DIV',]),
    ]
)

@pg.production("main : program")
def main_program(self, p):
    return p[0]

@pg.production('program : NEWLINE program')
def ignore_first_newline(state, p):
    return p[1]

# @pg.production('suite: NEWLINE INDENT block DEDENT')
# def indent_stmt(state, p):
#     return p[2]

@pg.production('program : stmt_full')
def program_stmt(state, p):
    return Program(p[0])

@pg.production('program : stmt_full program')
def program_stmt_program(state, p):
    if type(p[1]) is Program:
        program = p[1]
    else:
        program = Program(p[12])
    
    program.add_statement(p[0])
    return p[1]

@pg.production('block : stmt_full')
def block_expr(state, p):
    return Block(p[0])


@pg.production('block : stmt_full block')
def block_expr_block(state, p):
    if type(p[1]) is Block:
        b = p[1]
    else:
        b = Block(p[1])
    
    b.add_statement(p[0])
    return b


@pg.production('stmt_full : stmt NEWLINE')
@pg.production('stmt_full : stmt $end')
def stmt_full(state, p):
    return p[0]

@pg.production('stmt : expr')
def stmt_expr(state, p):
    return p[0]

@pg.production('stmt : IDENTIFIER = expr')
def stmt_assignment(state, p):
    return Assignment(Variable(p[0].getstr()),p[2])

@pg.production('stmt : IDENTIFIER ( arglist ) COLON NEWLINE block END')
def stmt_func_def(state, p):
    return FunctionDeclaration(p[0].getstr(), Array(p[2]), p[6])

@pg.production('stmt : IDENTIFIER ( ) COLON NEWLINE block END')
def stmt_func_noargs_def(state, p):
    return FunctionDeclaration(p[0].getstr(), Null(), p[5])

@pg.production('const : FLOAT')
def expr_float(state, p):
    return Float(float(p[0].getstr()))

@pg.production('const : BOOLEAN')
def expr_boolean(state, p):
    return Boolean(True if p[0].getstr() == 'true' else False)

@pg.production('const : INTEGER')
def expr_integer(state, p):
    return Integer(int(p[0].getstr()))

@pg.production('const : STRING')
def expr_string(state, p):
    return String(p[0].getstr().strip('"\''))

@pg.production('expr : const')
def expr_const(state, p):
    return p[0]

@pg.production('expr : [ expr ]')
def expr_array_single(state, p):
    return Array(InnerArray([p[1]]))

@pg.production('expr : [ exprlist ]')
def expr_array(state, p):
    return Array(p[1])

@pg.production('exprlist : expr')
@pg.production('exprlist : expr ,')
def exprlist_single(state, p):
    return InnerArray([p[0]])

@pg.production('exprlist : exprlist , expr')
def exprlist(state, p):
    # exprlist should already be an InnerArray
    p[0].push(p[2])
    return p[0]

@pg.production('arglist : IDENTIFIER')
@pg.production('arglist : IDENTIFIER ,')
def arglist_single(state, p):
    return InnerArray([Variable(p[0].getstr())])

@pg.production('arglist : arglist , IDENTIFIER')
def arglist(state, p):
    # list should already be an InnerArray
    p[0].push(Variable(p[2].getstr()))
    return p[0]

@pg.production('maplist : IDENTIFIER COLON expr')
@pg.production('maplist : IDENTIFIER COLON expr ,')
def maplist_single(state, p):
    return InnerDict({ p[0]: p[2] })

@pg.production('maplist : IDENTIFIER COLON expr , maplist')
def arglist(state, p):
    # exprlist should already be an InnerArray
    p[4].update(p[0],p[2])
    return p[4]

@pg.production('expr : { maplist }')
def expr_dict(state, p):
    return Dict(p[1])

@pg.production('expr : expr [ expr ]')
def expr_array_index(state, p):
    return Index(p[0],p[2])

@pg.production('expr : IF expr COLON stmt END')
def expr_if_single_line(state, p):
    return If(condition=p[1],body=p[3])

@pg.production('expr : IF expr COLON stmt ELSE COLON stmt END')
def expr_if_else_single_line(state, p):
    return If(condition=p[1],body=p[3],else_body=p[6])

@pg.production('expr : IF expr NEWLINE block END')
def expr_if(state, p):
    return If(condition=p[1],body=p[3])

@pg.production('expr : IF expr NEWLINE block ELSE NEWLINE block END')
def expr_if_else(state, p):
    return If(condition=p[1],body=p[3],else_body=p[6])

@pg.production('expr : WHILE expr NEWLINE block END')
def expr_while(state, p):
    return While(condition=p[1],body=p[4])

@pg.production('expr : IDENTIFIER')
def expr_variable(state, p):
    # cannot return the value of a variable if it isn't yet defined
    return Variable(p[0].getstr())

@pg.production('expr : IDENTIFIER ( )')
def expr_call_noargs(state, p):
    # cannot return the value of a variable if it isn't yet defined
    return Call(p[0].getstr(),InnerArray())

@pg.production('expr : IDENTIFIER ( exprlist )')
def expr_call_args(state, p):
    # cannot return the value of a variable if it isn't yet defined
    return Call(p[0].getstr(),p[2])

@pg.production('expr : NOT expr ')
def expr_not(state, p):
    return Not(p[1])

@pg.production('expr : ( expr )')
def expr_parens(state, p):
    return p[1]

@pg.production('expr : expr PLUS expr')
@pg.production('expr : expr MINUS expr')
@pg.production('expr : expr MUL expr')
@pg.production('expr : expr DIV expr')
def expr_binop(state, p):
    left = p[0]
    right = p[2]
    token = p[1].gettokentype()

    if   token == 'PLUS':  return Add(left, right)
    elif token == 'MINUS': return Sub(left, right)
    elif token == 'MUL':   return Mul(left, right)
    elif token == 'DIV':   return Div(left, right)
    else: raise LogicError('Oops, this should not be possible!')
    
@pg.production('expr : expr != expr')
@pg.production('expr : expr == expr')
@pg.production('expr : expr >= expr')
@pg.production('expr : expr <= expr')
@pg.production('expr : expr > expr')
@pg.production('expr : expr < expr')
@pg.production('expr : expr AND expr')
@pg.production('expr : expr OR expr')
def expr_equality(state, p):
    left = p[0]
    right = p[2]
    check = p[1]
    token = check.gettokentype()
    
    if   token == '==':  return Equal(left, right)
    elif token == '!=':  return NotEqual(left, right)
    elif token == '>=':  return GreaterThanEqual(left, right)
    elif token == '<=':  return LessThanEqual(left, right)
    elif token == '>':   return GreaterThan(left, right)
    elif token == '<':   return LessThan(left, right)
    elif token == 'AND': return And(left, right)
    elif token == 'OR':  return Or(left, right)
    else: raise LogicError("Shouldn't be possible")

@pg.error
def error_handler(state, token):
    # print the token for debug
    pos = token.getsourcepos()
    if pos:
        raise UnexpectedTokenError(token.gettokentype(), pos)
    elif token.gettokentype() == '$end':
        raise UnexpectedEndError()
    else:
        raise UnexpectedTokenError(token.gettokentype(), None)

parser = pg.build()
state = ParserState()

def parse(code, state=state):
    result = parser.parse(lexer.lex(code), state)
    return result

