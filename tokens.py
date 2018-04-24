from enum import Enum


class TokenType(Enum):
    UNKNOWN = 0
    IDENTIFIER = 1
    CONSTANT = 2
    DOUBLE_OPERATOR = 3
    SINGLE_OPERATOR = 4
    OPENING_BRACKET = 5
    CLOSING_BRACKET = 6


class Token(str):

    def __new__(cls, value: str, position: int, type: TokenType):
        return super(Token, cls).__new__(cls, value)

    def __init__(self, value:str , position: int, type: TokenType):
        super().__init__()
        self.position = position
        self.type = type
