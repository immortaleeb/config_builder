import argparse
import importlib
import re
import os

from .parser import parse
from .context import ContainerContext

def parse_arguments(argv):
    parser = argparse.ArgumentParser(description='builds config files from templates')
    parser.add_argument('-t', '--template', dest='template', help='template file', required=True)

    return parser.parse_args(argv)

def load_config(config_file):
    config_module = re.sub('.py$', '', config_file)
    config = importlib.import_module(config_module, os.getcwd())

    variable_containers = {}

    for container_name, container_data in config.VARIABLE_CONTAINERS.items():
        container_class = container_data['class']
        container_config = container_data['config']

        container_instance = container_class(container_name, container_config)

        variable_containers[container_name] = container_instance

    return variable_containers

def resolve_variable(variable_containers, variable_reference):
    container_instance = variable_containers[variable_reference.container]
    context = ContainerContext(variable_containers)

    return container_instance.resolve(variable_reference.path, context)

def main(argv=None):
    args = parse_arguments(argv)

    variable_containers = load_config('config.py')

    with open(args.template) as file:
        variables = parse(file)
        for variable in variables:
            print(variable, resolve_variable(variable_containers, variable))

if __name__ == '__main__':
    main()

