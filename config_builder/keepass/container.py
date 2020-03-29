from pykeepass import PyKeePass

from .path import KeePassEntryPath

class KeePassContainer:
    def __init__(self, name, config):
        self.name = name
        self.keepass = PyKeePass(config['db_path'], password=config['db_password'])

    def resolve(self, path):
        keepass_path = KeePassEntryPath.parse(path)

        entry = self.keepass.find_entries(path=keepass_path.path, first=True)
        return self.resolve_attribute(entry, keepass_path.attribute)

    def resolve_attribute(self, entry, entry_attribute):
        if (hasattr(entry, entry_attribute)):
            return getattr(entry, entry_attribute)
        else:
            raise Exception('Could not resolve unknown property \'%s\'' % (entry_attribute,))
