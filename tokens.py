from enum import Enum
from typing import List
import math
import string


class TokenType(Enum):
    """Enumeration of possible token types with their specification - possible chars and max length of token"""

    OPENING_BRACKET = (1,           "(")
    CLOSING_BRACKET = (1,           ")")
    SINGLE_OPERATOR = (1,           "~")
    DOUBLE_OPERATOR = (1,           "|&^>=")
    CONSTANT        = (1,           "01")
    IDENTIFIER      = (math.inf,    string.ascii_letters + string.digits)
    WHITESPACE      = (math.inf,    string.whitespace)
    UNKNOWN         = (1,           "")

    def __init__(self, max_length: int, chars: str):
        self.max_length = max_length
        self.chars = chars


class Token(str):
    """Extension of string that adds token type and position parameters"""

    def __new__(cls, value: str, type: TokenType, position: int = 0):
        return super(Token, cls).__new__(cls, value)

    def __init__(self, value:str, type: TokenType, position: int = 0):
        super().__init__()
        self.position = position
        self.type = type


def get_token(exp: str) -> Token:
    """Returns first token present in given expression"""

    length = 0
    for type in TokenType:
        while length < len(exp) and length < type.max_length and exp[length] in type.chars:
            length += 1
        if length > 0:
            return Token(exp[:length], type)
    return Token(exp[0], TokenType.UNKNOWN)


def tokenize(exp: str) -> List[Token]:
    """Returns list of tokens present in given expression"""

    tokens = []
    i = 0
    while i < len(exp):
        tokens.append(get_token(exp[i:]))
        tokens[-1].position = i
        i += len(tokens[-1])
    return tokens
