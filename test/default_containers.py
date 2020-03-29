import unittest

from config_builder.container import FixedContainer, DictContainer, ProxyContainer
from config_builder.context import ContainerContext

NO_CONTEXT = None

class FixedContainerTest(unittest.TestCase):
    def test_resolve_returns_None_for_unknown_path(self):
        container = FixedContainer('example', {})

        self.assertEqual(container.resolve('/unknown/path', NO_CONTEXT), None)

    def test_resolve_returns_path_value(self):
        container = FixedContainer('example', { 'example/credentials/@password': 'MySecret' })

        self.assertEqual(container.resolve('example/credentials/@password', NO_CONTEXT), 'MySecret')

class DictContainerTest(unittest.TestCase):
    def test_resolve_returns_None_for_unknown_path(self):
        container = DictContainer('example', {})

        self.assertEqual(container.resolve('/unknown/path', NO_CONTEXT), None)

    def test_resolves_recursive_dictionaries(self):
        container = DictContainer('example', {
            'databases': {
                'example-database': {
                    'user': 'example-user',
                    'pass': 'secret'
                }
            }
        })

        self.assertEqual(container.resolve('databases/example-database/user', NO_CONTEXT), 'example-user')
        self.assertEqual(container.resolve('databases/example-database/pass', NO_CONTEXT), 'secret')

class ProxyContainerTest(unittest.TestCase):
    def test_proxy_container_proxies_path(self):
        # given
        dict_container = FixedContainer('example-dict', { 'examples/password' : 'mysecret!' })
        proxy_container = ProxyContainer('example-proxy', {
            'proxied_container': 'example-dict',
            'bindings': {
                'my-password': 'examples/password'
            }
        })

        context = ContainerContext({
            'example-dict': dict_container,
            'example-proxy': proxy_container,
        })

        # when
        resolved_variable = proxy_container.resolve('my-password', context)

        # then
        self.assertEqual(resolved_variable, 'mysecret!')

    def test_proxy_container_ignores_attributes(self):
        # given
        dict_container = FixedContainer('example-dict', { 'examples/credentials/@password': 'mysecret!' })
        proxy_container = ProxyContainer('example-proxy', {
            'proxied_container': 'example-dict',
            'bindings': {
                'my-credentials': 'examples/credentials'
            }
        })

        context = ContainerContext({
            'example-dict': dict_container,
            'example-proxy': proxy_container,
        })

        # when
        resolved_variable = proxy_container.resolve('my-credentials/@password', context)

        # then
        self.assertEqual(resolved_variable, 'mysecret!')

    def test_proxy_container_proxies_prefixes(self):
        # given
        dict_container = FixedContainer('example-dict', { '/some/path/to/databases/my-database/@password' : 'mysecret!' })
        proxy_container = ProxyContainer('example-proxy', {
            'proxied_container': 'example-dict',
            'bindings': {
                'databases': '/some/path/to/databases'
            }
        })

        context = ContainerContext({
            'example-dict': dict_container,
            'example-proxy': proxy_container,
        })

        # when
        resolved_variable = proxy_container.resolve('databases/my-database/@password', context)

        # then
        self.assertEqual(resolved_variable, 'mysecret!')

    def test_proxy_container_proxies_longest_prefix(self):
        # given
        dict_container = FixedContainer('example-dict', {
            '/some/path/to/databases/my-database/@password' : 'wrongpassword',
            '/some/path/to/databases/my-database[1]/@password' : 'correctpassword'
        })
        proxy_container = ProxyContainer('example-proxy', {
            'proxied_container': 'example-dict',
            'bindings': {
                'databases': '/some/path/to/databases',
                'databases/my-database': '/some/path/to/databases/my-database[1]'
            }
        })

        context = ContainerContext({
            'example-dict': dict_container,
            'example-proxy': proxy_container,
        })

        # when
        resolved_variable = proxy_container.resolve('databases/my-database/@password', context)

        # then
        self.assertEqual(resolved_variable, 'correctpassword')


if __name__ == '__main__':
    unittest.main()
