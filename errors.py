class LogicError(Exception):
    def __str__(self):
        return self.message


class UnexpectedEndError(Exception):
    message = 'Unexpected end of statement'
    
    def __str__(self):
        return self.message


class UnexpectedTokenError(Exception):
    def __init__(self, token, pos):
        self.token = token
        self.pos = pos

    def __str__(self):
        return "[%s], line %d, col %d" % (self.token, self.pos.lineno, self.pos.colno)


class ImmutableError(Exception):
    message = 'Cannot assign to immutable variable %s'

    def __init__(self, name):
        self.name = name
        
    def __str__(self):
        return self.message % self.name
