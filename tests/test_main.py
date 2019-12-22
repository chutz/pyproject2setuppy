# vim:se fileencoding=utf-8 :
# (c) 2019 Michał Górny
# 2-clause BSD license

import os
import sys
import unittest

if sys.hexversion >= 0x03000000:
    from tempfile import TemporaryDirectory
    from unittest.mock import patch
else:
    from backports.tempfile import TemporaryDirectory
    from mock import patch

from pyproject2setuppy.main import main


def make_pyproject_toml(data):
    d = TemporaryDirectory()
    os.chdir(d.name)
    with open('pyproject.toml', 'w') as f:
        f.write(data)
    return d


class MainUnitTest(unittest.TestCase):
    @patch('pyproject2setuppy.flit.handle_flit')
    def test_flit(self, handler_mock):
        data = '''
[build-system]
requires = ["flit"]
build-backend = "flit.buildapi"
'''
        with make_pyproject_toml(data):
            main()
            self.assertTrue(handler_mock.called)

    @patch('pyproject2setuppy.poetry.handle_poetry')
    def test_poetry(self, handler_mock):
        data = '''
[build-system]
requires = ["poetry"]
build-backend = "poetry.masonry.api"
'''
        with make_pyproject_toml(data):
            main()
            self.assertTrue(handler_mock.called)

    def test_garbage(self):
        data = '''
[build-system]
build-backend = "pyproject2setuppy.garbage"
'''
        with make_pyproject_toml(data):
            self.assertRaises(NotImplementedError, main)
