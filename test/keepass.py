import unittest

from config_builder.keepass.path import KeePassEntryPath

class KeePassEntryTest(unittest.TestCase):

    def test_parse_parses_path_and_attribute(self):
        entry = KeePassEntryPath.parse('My Secrets/Databases/example-postgres/@password')

        self.assertEqual(entry.path, 'My Secrets/Databases/example-postgres')
        self.assertEqual(entry.attribute, 'password')

    def test_parses_entry_index(self):
        entry = KeePassEntryPath.parse('database/example[2]/@username')

        self.assertEqual(entry.index, 2)

if __name__ == '__main__':
    unittest.main()

