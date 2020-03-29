import re

KEEPASS_ENTRY_PATH_REGEX = r'^(?:(?P<group_path>[^[]+)/)?(?P<title>[^]]+)(?:\[(?P<index>[0-9]+)\])?/@(?P<attribute>.+)$'

class KeePassEntryPath:
    def __init__(self, group_path, title, index, attribute):
        self.group_path = group_path
        self.title = title
        self.index = index
        self.attribute = attribute

    @classmethod
    def parse(cls, path):
        match = re.match(KEEPASS_ENTRY_PATH_REGEX, path)

        if not match:
           raise Exception('Could not parse entry \'%s\'' % (path))

        group_path = match.group('group_path')
        entry_title = match.group('title')
        entry_index = int(match.group('index') or '0')
        entry_attribute = match.group('attribute')

        return cls(group_path, entry_title, entry_index, entry_attribute)

