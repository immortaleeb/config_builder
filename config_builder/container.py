class DictContainer:
    def __init__(self, name, config):
        self.name = name
        self.config = config

    def resolve(self, path):
        return self.config[path] if path in self.config else None

