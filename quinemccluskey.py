from itertools import combinations
from functools import reduce
from typing import List, Dict, Tuple, Set, Optional

from tokens import Token, TokenType
from exceptions import SyntaxException, MissingVariableException

# type aliases
Expression = List[Token]
TestCase = Dict[str, bool]
Implicant = Tuple[Set[int], str]


def check_syntax(exp: Expression):
    """Checks syntax of given expression and throws SyntaxExceptions if needed"""

    indent = 0
    state = 1

    # for every token
    for tok in exp:

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
        raise SyntaxException(exp[-1], "Missing closing bracket")

    # checks final state
    if state != 2:
        raise SyntaxException(exp[-1], "Unexpected end of statement")


def _to_rpn(exp: Expression) -> Expression:
    """Parses expression to rpn format"""

    queue = []
    stack = []

    for tok in exp:

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


def _get_variables(exp: Expression) -> Expression:
    """Returns all variables present in expression, sorted, without duplicates"""
    return sorted(set([tok for tok in exp if tok.type is TokenType.IDENTIFIER]))


def _get_test_case(vars: List[str], ite: int) -> TestCase:
    """Returns test case for given variables, where values are calculated from given iterator"""
    return {vars[i]: ((ite >> i) % 2 > 0) for i in range(len(vars))}


def _evaluate(exp: Expression, variables: TestCase) -> bool:
    """Evaluates expression with given test case"""

    stack = []

    for tok in exp:

        if tok.type is TokenType.CONSTANT:
            stack.append(tok == '1')
            continue

        if tok.type is TokenType.IDENTIFIER:
            if tok not in variables:
                raise MissingVariableException(tok)
            stack.append(variables[tok])
            continue

        if tok.type in [TokenType.SINGLE_OPERATOR, TokenType.DOUBLE_OPERATOR]:

            if tok == '~':
                stack = stack[:-1] + [ not stack[-1] ]
                continue

            if tok == '|':
                stack = stack[:-2] + [ stack[-2] or stack[-1] ]
                continue

            if tok == '&':
                stack = stack[:-2] + [ stack[-2] and stack[-1] ]
                continue

            if tok == '=':
                stack = stack[:-2] + [ stack[-2] == stack[-1] ]
                continue

            if tok == '^':
                stack = stack[:-2] + [ stack[-2] != stack[-1] ]
                continue

            if tok == '>':
                stack = stack[:-2] + [ (not stack[-2]) or stack[-1] ]
                continue

        raise SyntaxError(tok, "Unexpected token in RPN format")

    return stack[0]


def _get_minterms(exp: Expression, vars: List[str]) -> List[int]:
    """Returns all minterms from expression with given variables"""
    return [i for i in range(1 << len(vars)) if _evaluate(exp, _get_test_case(vars, i))]


def _get_bitmask(ite: int, size: int) -> str:
    return bin(ite)[2:].rjust(size,'0')


def _get_difference(mask1: str, mask2: str) -> int:
    return len([True for b1, b2 in zip(mask1, mask2) if b1 != b2])


def _merge_bitmasks(mask1: str, mask2: str) -> str:
    mask = ""
    for b1, b2 in zip(mask1, mask2):
        mask += ('-' if b1 != b2 else b1)
    return mask


def _merge_implicants(imp1: Implicant, imp2: Implicant) -> Implicant:
    return imp1[0] | imp2[0], _merge_bitmasks(imp1[1], imp2[1])


def _get_implicants(minterms: List[int], size: int) -> List[Implicant]:
    return [({m}, _get_bitmask(m, size)) for m in minterms]


def _get_prime_implicants(implicants: List[Implicant]) -> List[Implicant]:

    prime = []

    while True:
        used = set()
        created = []

        # merge all possible implicants
        for imp1, imp2 in combinations(implicants, 2):

            if _get_difference(imp1[1], imp2[1]) != 1:
                continue

            created.append(_merge_implicants(imp1, imp2))
            used.add(imp1[1])
            used.add(imp2[1])

        # add all not used implicants are prime
        for imp in implicants:
            if imp[1] not in used:
                prime.append(imp)

        if len(created) == 0:
            break

        implicants = created

    return prime


def _get_smallest_prime_set(implicants: List[Implicant], minterms: List[int]) -> Optional[List[Implicant]]:
    for i in range(1, 1 + len(minterms)):
        for prime_set in combinations(implicants, i):

            # merge
            prime_minterms = set()
            for mins, _ in prime_set:
                prime_minterms = prime_minterms.union(mins)

            if all(p in prime_minterms for p in minterms):
                return prime_set
    return None


def _get_single_expression(impl: Implicant, variables: List[str]) -> Expression:
    exp = []
    for i in range(len(impl[1])):
        if impl[1][i] == '0':
            exp.append(Token('~', TokenType.SINGLE_OPERATOR))
        if impl[1][i] in '01':
            exp.append(Token(variables[i], TokenType.IDENTIFIER))
    return exp


def _get_expression(implicants: List[Implicant], variables: List[str]) -> Expression:
    return reduce(lambda a, b: a + [Token('|', TokenType.DOUBLE_OPERATOR)] + b, [_get_single_expression(impl, variables) for impl in implicants])




def simplify(expression: Expression) -> Expression:
    """Returns simplified expression, input expression should be in normal (not rpn) format"""

    # parse to rpn
    expression = _to_rpn(expression)

    # get variables
    variables = _get_variables(expression)

    # if there is no variables nothing to simplify
    if len(variables) == 0:
        if _evaluate(expression, {}):
            return [Token('1', TokenType.CONSTANT)]
        else:
            return [Token('0', TokenType.CONSTANT)]

    # get all minterms
    minterms = _get_minterms(expression, variables)

    # if there are not minterms its always false
    if len(minterms) == 0:
        return [Token('0', TokenType.CONSTANT)]

    # if there is as many minterms as test cases its always true
    if len(minterms) == (1 << len(variables)):
        return [Token('1', TokenType.CONSTANT)]

    # get implicants
    implicants = _get_implicants(minterms, len(variables))

    # get prime implicants
    implicants = _get_prime_implicants(implicants)

    # get prime set
    implicants = _get_smallest_prime_set(implicants, minterms)

    # return expression
    return _get_expression(implicants, variables)


