from typing import List

from exceptions import SyntaxException
from tokens import Token, TokenType
import syntax


def tokenize(exp: str) -> List[Token]:
    tokens = []

    i = 0
    while i < len(exp):

        if exp[i] in syntax.WHITE_CHARS:
            i += 1

        elif exp[i] in syntax.CONSTANTS:
            tokens.append(Token(exp[i], i, TokenType.CONSTANT))
            i += 1

        elif exp[i] in syntax.SINGLE_OPERATORS:
            tokens.append(Token(exp[i], i, TokenType.SINGLE_OPERATOR))
            i += 1

        elif exp[i] in syntax.DOUBLE_OPERATORS:
            tokens.append(Token(exp[i], i, TokenType.DOUBLE_OPERATOR))
            i += 1

        elif exp[i] == syntax.OPENING_BRACKET:
            tokens.append(Token(exp[i], i, TokenType.OPENING_BRACKET))
            i += 1

        elif exp[i] == syntax.CLOSING_BRACKET:
            tokens.append(Token(exp[i], i, TokenType.CLOSING_BRACKET))
            i += 1

        elif exp[i] in syntax.IDENTIFIERS:
            j = i + 1
            while j < len(exp) and exp[j] in syntax.IDENTIFIERS:
                j += 1
            tokens.append(Token(exp[i:j], i, TokenType.IDENTIFIER))
            i = j

        else:
            tokens.append(Token(exp[i], i, TokenType.UNKNOWN))
            i += 1

    return tokens


def check_syntax(tokens: List[Token]):

    indent = 0
    state = 1

    for tok in tokens:
        if state == 1:

            if tok.type is TokenType.IDENTIFIER:
                state = 2

            elif tok.type is TokenType.OPENING_BRACKET:
                indent += 1

            elif tok.type is TokenType.SINGLE_OPERATOR:
                state = 1

            elif tok.type is TokenType.CONSTANT:
                state = 2

            else:
                raise SyntaxException(tok.position, "Unexpected token '" + tok + "'")

        else:

            if tok.type is TokenType.CLOSING_BRACKET:
                indent -= 1
                if indent < 0:
                    raise SyntaxException(tok.position, "Unexpected closing bracket")

            elif tok.type is TokenType.DOUBLE_OPERATOR:
                state = 1

            else:
                raise SyntaxException(tok.position, "Unexpected token '" + tok + "'")

    if indent is not 0:
        raise SyntaxException(tokens[-1].position + len(tokens[-1]), "Missing closing bracket")


def to_rpn(tokens: List[Token]) -> List[Token]:

    queue = []
    stack = []

    for tok in tokens:

        # any variable or constant -> to queue
        if tok.type in [TokenType.IDENTIFIER, TokenType.CONSTANT]:
            queue.append(tok)

        # opening racket -> to stack
        elif tok.type is TokenType.OPENING_BRACKET:
            stack.append(tok)

        # closing bracket -> move form stack to queue
        elif tok.type is TokenType.CLOSING_BRACKET:
            while stack[-1].type is not TokenType.OPENING_BRACKET:
                queue.append(stack.pop())
            stack.pop()

        # operators -> complicated
        elif tok.type in [TokenType.DOUBLE_OPERATOR, TokenType.SINGLE_OPERATOR]:
            while len(stack) > 0 and stack[-1].type is not TokenType.OPENING_BRACKET and (syntax.PRECEDENCES[stack[-1]] > syntax.PRECEDENCES[tok] or (syntax.PRECEDENCES[stack[-1]] == syntax.PRECEDENCES[tok] and stack[-1].type is TokenType.SINGLE_OPERATOR)):
                queue.append(stack.pop())
            stack.append(tok)

        # other -> error
        else:
            raise SyntaxException(tok.position, "Unexpected token '" + tok + "'")

    while len(stack) > 0:
        queue.append(stack.pop())

    return queue
