import re

KEEPASS_ENTRY_PATH_REGEX = r'^(?P<path>[^[]*)(?:\[(?P<index>[0-9]+)\])?/@(?P<attribute>.+)$'

class KeePassEntryPath:
    def __init__(self, path, index, attribute):
        self.path = path
        self.index = index
        self.attribute = attribute

    @classmethod
    def parse(cls, path):
        match = re.match(KEEPASS_ENTRY_PATH_REGEX, path)

        if not match:
           raise Exception('Could not parse entry \'%s\'' % (path))

        entry_path = match.group('path')
        entry_index = int(match.group('index') or '0')
        entry_attribute = match.group('attribute')

        return cls(entry_path, entry_index, entry_attribute)
