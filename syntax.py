import string
from collections import defaultdict

# SYNTAX SETTINGS
PRECEDENCES                     = defaultdict(lambda: 0)

WHITE_CHARS                     = list(string.whitespace)

IDENTIFIERS                     = list(string.ascii_letters + string.digits)

OPENING_BRACKET                 = '('
PRECEDENCES[OPENING_BRACKET]    = 10

CLOSING_BRACKET                 = ')'
PRECEDENCES[CLOSING_BRACKET]    = 10

BRACKETS                        = [OPENING_BRACKET, CLOSING_BRACKET]

AND_OPERATOR                    = '&'
PRECEDENCES[AND_OPERATOR]       = 4

OR_OPERATOR                     = '|'
PRECEDENCES[OR_OPERATOR]        = 3

XOR_OPERATOR                    = '^'
PRECEDENCES[XOR_OPERATOR]       = 5

NOT_OPERATOR                    = '~'
PRECEDENCES[NOT_OPERATOR]       = 6

IMPL_OPERATOR                   = '>'
PRECEDENCES[IMPL_OPERATOR]      = 2

XNOR_OPERATOR                   = '='
PRECEDENCES[XNOR_OPERATOR]      = 1

SINGLE_OPERATORS                = [NOT_OPERATOR]
DOUBLE_OPERATORS                = [AND_OPERATOR, OR_OPERATOR, XOR_OPERATOR, IMPL_OPERATOR, XOR_OPERATOR]
OPERATORS                       = SINGLE_OPERATORS + DOUBLE_OPERATORS

TRUE_CONSTANT                   = '1'
FALSE_CONSTANT                  = '0'
CONSTANTS                       = [TRUE_CONSTANT, FALSE_CONSTANT]

VALID_CHARS                     = WHITE_CHARS + IDENTIFIERS + BRACKETS + OPERATORS + CONSTANTS
