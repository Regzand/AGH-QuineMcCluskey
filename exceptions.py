
class MissingVariableException(Exception):

    def __init__(self, variable_name: str):
        self.variable_name = variable_name

    def __str__(self) -> str:
        return "Missing variable '" + self.variable_name + "'"


class SyntaxException(Exception):

    def __init__(self, position: int, msg: str):
        self.position = position
        self.msg = msg

    def __str__(self):
        return "Syntax error at " + str(self.position) + ": " + self.msg
