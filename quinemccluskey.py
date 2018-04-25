from typing import List

from tokens import Token, TokenType
from exceptions import SyntaxException


def check_syntax(tokens: List[Token]):
    """Checks syntax of given expression and throws SyntaxExceptions if needed"""

    indent = 0
    state = 1

    # for every token
    for tok in tokens:

        # skips whitespaces
        if tok.type is TokenType.WHITESPACE:
            continue

        # if in state 1
        if state == 1:

            # identifier -> ok, state 2
            if tok.type is TokenType.IDENTIFIER:
                state = 2

            # opening bracket -> ok, state 1
            elif tok.type is TokenType.OPENING_BRACKET:
                indent += 1
                state = 1

            # single operator -> ok, state 1
            elif tok.type is TokenType.SINGLE_OPERATOR:
                state = 1

            # constatnt -> ok, state 2
            elif tok.type is TokenType.CONSTANT:
                state = 2

            # anything else -> error
            else:
                raise SyntaxException(tok, "Unexpected token")

        # if in state 2
        else:

            # closing bracket -> check indentation, state 2
            if tok.type is TokenType.CLOSING_BRACKET:
                indent -= 1
                state = 2
                if indent < 0:
                    raise SyntaxException(tok, "Unexpected closing bracket")

            # double operator -> ok, state 1
            elif tok.type is TokenType.DOUBLE_OPERATOR:
                state = 1

            # anything else -> error
            else:
                raise SyntaxException(tok, "Unexpected token")

    # checks final indentation
    if indent != 0:
        raise SyntaxException(tokens[-1], "Missing closing bracket")

    # checks final state
    if state != 2:
        raise SyntaxException(tokens[-1], "Unexpected end of statement")


def to_rpn(tokens: List[Token]) -> List[Token]:
    """Parses expression to rpn format"""

    queue = []
    stack = []

    for tok in tokens:

        # skips whitespaces
        if tok.type is TokenType.WHITESPACE:
            continue

        # any variable or constant -> to queue
        if tok.type in [TokenType.IDENTIFIER, TokenType.CONSTANT]:
            queue.append(tok)
            continue

        # opening bracket -> to stack
        if tok.type is TokenType.OPENING_BRACKET:
            stack.append(tok)
            continue

        # closing bracket -> move form stack to queue
        if tok.type is TokenType.CLOSING_BRACKET:
            while stack[-1].type is not TokenType.OPENING_BRACKET:
                queue.append(stack.pop())
            stack.pop()
            continue

        # operators -> complicated xD
        if tok.type in [TokenType.DOUBLE_OPERATOR, TokenType.SINGLE_OPERATOR]:
            while len(stack) > 0 and stack[-1].type is not TokenType.OPENING_BRACKET and (stack[-1].precedence > tok.precedence or (stack[-1].precedence == tok.precedence and stack[-1].type is TokenType.SINGLE_OPERATOR)):
                queue.append(stack.pop())
            stack.append(tok)
            continue

        # other -> error
        raise SyntaxException(tok, "Unexpected token")

    # move everything from stack to queue
    while len(stack) > 0:
        queue.append(stack.pop())

    # return queue - expression in rpn format
    return queue
