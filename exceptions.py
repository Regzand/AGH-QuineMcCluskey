from tokens import Token


class MissingVariableException(Exception):

    def __init__(self, variable_name: str):
        self.variable_name = variable_name

    def __str__(self) -> str:
        return "Missing variable '" + self.variable_name + "'"


class SyntaxException(Exception):

    def __init__(self, token: Token, msg: str):
        self.token = token
        self.msg = msg

    def __str__(self):
        return "Syntax error at position" + str(self.token.position) + " (" + self.token + "): " + self.msg
