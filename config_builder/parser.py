import re
import functools

VARIABLE_REGEX=r'\$\{([^}]+)\}'
VARIABLE_FORMAT="${%s}"

VARIABLE_REFERENCE_REGEX=r'^(.+)://(.+)$'
VARIABLE_REFERENCE_FORMAT='%s://%s'

class VariableReference:
    def __init__(self, container, path):
        self.container = container
        self.path = path

    def __str__(self):
        return "(container: %s, path: %s)" % (self.container, self.path)

class VariableBinding:
    def __init__(self, reference, value):
        self.reference = reference
        self.value = value

def parse_variables(template_file):
    all_variables = []
    for line in template_file:
        variables = re.finditer(VARIABLE_REGEX, line)
        for variable in variables:
            all_variables.append(variable.group(1))

    return all_variables

def parse_variable_reference(variable):
    try:
        match = re.match(VARIABLE_REFERENCE_REGEX, variable)
        return VariableReference(match.group(1), match.group(2))
    except Exception as e:
        raise Exception("Error while parsing variable " + variable, e)

def parse(template_file):
    variables = parse_variables(template_file)
    return [ parse_variable_reference(variable) for variable in variables ]

def compile(template_file, bindings):
    for line in template_file:
        variable_matches = re.finditer(VARIABLE_REGEX, line)
        compiled_line = line

        for variable_match in variable_matches:
            variable = variable_match.group(1)
            binding = find_binding_for_variable(bindings, variable)
            if binding:
                compiled_line = compiled_line.replace(variable_to_string(variable), binding.value)
            else:
                print("WARNING: no binding found for variable '%s'" % (variable,))

        print(compiled_line, end='')

def find_binding_for_variable(bindings, variable):
    for binding in bindings:
        if variable == reference_to_string(binding.reference):
            return binding

    return None

def reference_to_string(reference):
    return VARIABLE_REFERENCE_FORMAT % (reference.container, reference.path)

def variable_to_string(variable):
    return VARIABLE_FORMAT % (variable,)

