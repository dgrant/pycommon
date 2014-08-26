import os

import unittest
from pycommon import experimental
from mock import patch, call

class Test_pathsplit(unittest.TestCase):

    def test_pathsplit_slashes(self):
        ret = experimental.pathsplit(os.path.sep + os.path.sep.join(['aa', 'b', 'cc']) + os.path.sep)
        self.assertEqual(ret, ['aa', 'b', 'cc'])

    def test_pathsplit_no_slashes(self):
        ret = experimental.pathsplit(os.path.sep.join(['a', 'bb', 'cc']))
        self.assertEqual(ret, ['a', 'bb', 'cc'])

    def test_pathsplit_slashes(self):
        ret = experimental.pathsplit(os.path.sep + os.path.sep.join(['aa', 'b', 'cc']) + os.path.sep)
        self.assertEqual(ret, ['aa', 'b', 'cc'])

    def test_pathsplit_no_slashes(self):
        ret = experimental.pathsplit('.')
        self.assertEqual(ret, ['.'])

    def test_pathsplit_no_slashes(self):
        ret = experimental.pathsplit('.' + os.path.sep)
        self.assertEqual(ret, ['.'])


class Test_mkdir2(unittest.TestCase):

    @patch('os.makedirs')
    def test_mkdir(self, makedirs_mock):
        kwargs = {'exist_ok': True, 'mode': 511}
        experimental.mkdir(os.path.join('a', '{b,c}', 'd'), **kwargs)
        self.assertEqual(makedirs_mock.mock_calls, [
            call(os.path.join('a', 'b', 'd'), **kwargs),
            call(os.path.join('a', 'c', 'd'), **kwargs)])

    @patch('os.makedirs')
    def test_mkdir_complicated(self, makedirs_mock):
        kwargs = {'exist_ok': True, 'mode': 511}
        experimental.mkdir(os.path.join('a', '{b,c}', 'd', '{e,f}'), **kwargs)
        self.assertEqual(makedirs_mock.mock_calls, [
            call(os.path.join('a', 'b', 'd', 'e'), **kwargs),
            call(os.path.join('a', 'b', 'd', 'f'), **kwargs),
            call(os.path.join('a', 'c', 'd', 'e'), **kwargs),
            call(os.path.join('a', 'c', 'd', 'f'), **kwargs)])

    @patch('os.makedirs')
    def test_mkdir_no_expand_paths(self, makedirs_mock):
        kwargs = {'exist_ok': True, 'mode': 511}
        experimental.mkdir(os.path.join('a', '{b,c}', 'd'), expand_paths=False, **kwargs)
        self.assertEqual(makedirs_mock.mock_calls, [
            call(os.path.join('a', '{b,c}', 'd'), **kwargs),])


    def test_expand_paths(self):
        ret = experimental._expand_paths('a/b')
        self.assertEqual(ret, ['a/b'])

    def test_expand_paths1(self):
        ret = experimental._expand_paths('a')
        self.assertEqual(ret, ['a'])

    def test_expand_paths2(self):
        ret = experimental._expand_paths('{a,b,c}')
        self.assertEqual(ret, ['a', 'b', 'c'])

    def test_expand_paths3(self):
        ret = experimental._expand_paths('{a,b,c}/d')
        self.assertEqual(ret, ['a/d', 'b/d', 'c/d'])

    def test_expand_paths4(self):
        ret = experimental._expand_paths('a/{b,c,c}')
        self.assertEqual(ret, ['a/b', 'a/c', 'a/d'])

    def test_expand_paths4(self):
        ret = experimental._expand_paths('a/{b,c}/d')
        self.assertEqual(ret, ['a/b/d', 'a/c/d'])

    def test_expand_paths4(self):
        ret = experimental._expand_paths('a/{b,c}/d/{e,f}')
        self.assertEqual(['a/b/d/e', 'a/b/d/f', 'a/c/d/e', 'a/c/d/f'], ret)

    # def test_expand_paths5(self):
    #     ret = experimental._expand_paths('a{aa,bb}')
    #     self.assertEqual(['aaa', 'abb'], ret)
