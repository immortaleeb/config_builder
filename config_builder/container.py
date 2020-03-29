class DictContainer:
    def __init__(self, name, config):
        self.name = name
        self.config = config

    def resolve(self, path, context):
        return self.config[path] if path in self.config else None

class ProxyContainer:
    def __init__(self, name, config):
        self.name = name
        self.proxied_container = config['proxied_container']
        self.path_bindings = config['bindings']

    def resolve(self, path, context):
        if path in self.path_bindings:
            proxied_path = self.path_bindings[path]
        else:
            prefix = self.find_prefix_binding_for(path)

            if prefix:
                proxied_path = path.replace(prefix, self.path_bindings[prefix])
            else:
                proxied_path = path

        if self.proxied_container not in context.containers:
            raise Exception("Unknown container '%s'" % (self.proxied_container))

        proxied_container = context.containers[self.proxied_container]

        return proxied_container.resolve(proxied_path, context)

    def find_prefix_binding_for(self, path):
        longest_match = None

        for binding in self.path_bindings.keys():
            if path.startswith(binding):
                if not longest_match or len(longest_match) < len(binding):
                    longest_match = binding

        return binding

