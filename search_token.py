"""Token constants."""

__all__ = ['tok_name', 'ISTERMINAL', 'ISNONTERMINAL', 'ISEOF']

ENDMARKER = 0
WORD = 1
NUMBER = 2
STRING = 3
NEWLINE = 4
LPAR = 5
RPAR = 6
LSQB = 7
RSQB = 8
COLON = 9
COMMA = 10
SEMI = 11
PLUS = 12
MINUS = 13
STAR = 14
SLASH = 15
VBAR = 16
AMPER = 17
LESS = 18
GREATER = 19
EQUAL = 20
DOT = 21
PERCENT = 22
LBRACE = 23
RBRACE = 24
EQEQUAL = 25
NOTEQUAL = 26
LESSEQUAL = 27
GREATEREQUAL = 28
TILDE = 29
CIRCUMFLEX = 30
LEFTSHIFT = 31
RIGHTSHIFT = 32
DOUBLESTAR = 33
PLUSEQUAL = 34
MINEQUAL = 35
STAREQUAL = 36
SLASHEQUAL = 37
PERCENTEQUAL = 38
AMPEREQUAL = 39
VBAREQUAL = 40
CIRCUMFLEXEQUAL = 41
LEFTSHIFTEQUAL = 42
RIGHTSHIFTEQUAL = 43
DOUBLESTAREQUAL = 44
DOUBLESLASH = 45
DOUBLESLASHEQUAL = 46
AT = 47
ATEQUAL = 48
RARROW = 49
ELLIPSIS = 50
COLONEQUAL = 51
OP = 52
TYPE_IGNORE = 53
ERRORTOKEN = 54
ENCODING = 55
N_TOKENS = 56
# Special definitions for cooperation with parser
NT_OFFSET = 256

tok_name = {value: name
            for name, value in globals().items()
            if isinstance(value, int) and not name.startswith('_')}
__all__.extend(tok_name.values())

EXACT_TOKEN_TYPES = {
    '!=': NOTEQUAL,
    '%': PERCENT,
    '%=': PERCENTEQUAL,
    '&': AMPER,
    '&=': AMPEREQUAL,
    '(': LPAR,
    ')': RPAR,
    '*': STAR,
    '**': DOUBLESTAR,
    '**=': DOUBLESTAREQUAL,
    '*=': STAREQUAL,
    '+': PLUS,
    '+=': PLUSEQUAL,
    ',': COMMA,
    '-': MINUS,
    '-=': MINEQUAL,
    '->': RARROW,
    '.': DOT,
    '...': ELLIPSIS,
    '/': SLASH,
    '//': DOUBLESLASH,
    '//=': DOUBLESLASHEQUAL,
    '/=': SLASHEQUAL,
    ':': COLON,
    ':=': COLONEQUAL,
    ';': SEMI,
    '<': LESS,
    '<<': LEFTSHIFT,
    '<<=': LEFTSHIFTEQUAL,
    '<=': LESSEQUAL,
    '=': EQUAL,
    '==': EQEQUAL,
    '>': GREATER,
    '>=': GREATEREQUAL,
    '>>': RIGHTSHIFT,
    '>>=': RIGHTSHIFTEQUAL,
    '@': AT,
    '@=': ATEQUAL,
    '[': LSQB,
    ']': RSQB,
    '^': CIRCUMFLEX,
    '^=': CIRCUMFLEXEQUAL,
    '{': LBRACE,
    '|': VBAR,
    '|=': VBAREQUAL,
    '}': RBRACE,
    '~': TILDE,
}

def ISTERMINAL(x):
    return x < NT_OFFSET

def ISNONTERMINAL(x):
    return x >= NT_OFFSET

def ISEOF(x):
    return x == ENDMARKER