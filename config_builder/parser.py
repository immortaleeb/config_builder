import re
import functools

VARIABLE_REGEX=r'\$\{([^}]+)\}'
VARIABLE_REFERENCE_REGEX=r'^(.+)://(.+)$'

class VariableReference:
    def __init__(self, container, path):
        self.container = container
        self.path = path

    def __str__(self):
        return "(container: %s, path: %s)" % (self.container, self.path)

def parse_variables(file):
    all_variables = []
    for line in file:
        variables = re.finditer(VARIABLE_REGEX, line)
        for variable in variables:
            all_variables.append(variable.group(1))

    return all_variables

def parse_variabLe_reference(variable):
    match = re.match(VARIABLE_REFERENCE_REGEX, variable)
    return VariableReference(match.group(1), match.group(2))


def parse(file):
    variables = parse_variables(file)
    return [ parse_variabLe_reference(variable) for variable in variables ]

