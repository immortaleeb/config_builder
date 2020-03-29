import unittest

from config_builder.container import DictContainer

class DictContainerTest(unittest.TestCase):
    def test_resolve_returns_None_for_unknown_path(self):
        container = DictContainer('example', {})

        self.assertEqual(container.resolve('/unknown/path'), None)

if __name__ == '__main__':
    unittest.main()
