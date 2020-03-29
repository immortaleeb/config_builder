from pykeepass import PyKeePass

from .path import KeePassEntryPath

class KeePassContainer:
    def __init__(self, name, config):
        self.name = name
        self.keepass = PyKeePass(config['db_path'], password=config['db_password'])

    def resolve(self, path, context):
        keepass_path = KeePassEntryPath.parse(path)

        group = self.keepass.find_groups(path=keepass_path.group_path) if keepass_path.group_path else None
        entries = self.keepass.find_entries(title=keepass_path.title, group=group)

        if entries and keepass_path.index < len(entries):
            entry = entries[keepass_path.index]
            return self.resolve_attribute(entry, keepass_path.attribute)
        else:
            return None

    def resolve_attribute(self, entry, entry_attribute):
        if (hasattr(entry, entry_attribute)):
            return getattr(entry, entry_attribute)
        else:
            raise Exception('Could not resolve unknown property \'%s\'' % (entry_attribute,))

