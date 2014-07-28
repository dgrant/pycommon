import errno
import os
import unittest
from mock import patch, call

from pycommon import fileutil

class TestFileUtil_delete(unittest.TestCase):

    @patch('shutil.rmtree')
    @patch('os.path.isdir')
    def test_delete_dir(self, isdir_mock, rmtree_mock):
        # Setup
        dir_name = 'a_dir'
        isdir_mock.side_effect = lambda x: {dir_name: True}[x]

        # Call method-under-test
        fileutil.delete(dir_name)

        # Verification
        self.assertEqual(rmtree_mock.mock_calls, [call(dir_name)])

    @patch('os.remove')
    @patch('os.path.isdir')
    def test_delete_file(self, isdir_mock, remove_mock):
        # Setup
        file_name = 'a_file'
        isdir_mock.side_effect = lambda x: {file_name: False}[x]

        # Call method-under-test
        fileutil.delete(file_name)

        # Verification
        self.assertEqual(remove_mock.mock_calls, [call(file_name)])

    @patch('os.remove')
    @patch('shutil.rmtree')
    @patch('os.path.isdir')
    def test_delete_list(self, isdir_mock, rmtree_mock, remove_mock):
        # Setup
        dir_name = 'a_dir'
        file_name = 'a_file'
        isdir_mock.side_effect = lambda x: {file_name: False, dir_name: True}[x]

        # Call method-under-test
        fileutil.delete([file_name, dir_name])

        # Verification
        self.assertEqual(remove_mock.mock_calls, [call(file_name)])
        self.assertEqual(rmtree_mock.mock_calls, [call(dir_name)])

    @patch('os.remove')
    @patch('shutil.rmtree')
    @patch('os.path.isdir')
    def test_delete_list_neither_exists(self, isdir_mock, rmtree_mock, remove_mock):
        # Setup
        dir_name = 'a_dir'
        file_name = 'a_file'
        isdir_mock.side_effect = OSError(errno.ENOENT, 'does not exist')

        # Call method-under-test
        fileutil.delete([file_name, dir_name])

        # Verification
        # We should get here as no exception should have been thrown in the function

    @patch('os.remove')
    @patch('shutil.rmtree')
    @patch('os.path.isdir')
    def test_delete_list_random_exception(self, isdir_mock, rmtree_mock, remove_mock):
        # Setup
        dir_name = 'a_dir'
        file_name = 'a_file'
        isdir_mock.side_effect = OSError(errno.EACCES, 'permissions problem')

        # Call method-under-test
        self.assertRaises(OSError, fileutil.delete, [file_name, dir_name])



class Test_replace_in_file(unittest.TestCase):
    pass

class Test_pathsplit(unittest.TestCase):

    def test_pathsplit_slashes(self):
        ret = fileutil.pathsplit(os.path.sep + os.path.sep.join(['aa', 'b', 'cc']) + os.path.sep)
        self.assertEqual(ret, ['aa', 'b', 'cc'])

    def test_pathsplit_no_slashes(self):
        ret = fileutil.pathsplit(os.path.sep.join(['a', 'bb', 'cc']))
        self.assertEqual(ret, ['a', 'bb', 'cc'])

    def test_pathsplit_slashes(self):
        ret = fileutil.pathsplit(os.path.sep + os.path.sep.join(['aa', 'b', 'cc']) + os.path.sep)
        self.assertEqual(ret, ['aa', 'b', 'cc'])

    def test_pathsplit_no_slashes(self):
        ret = fileutil.pathsplit('.')
        self.assertEqual(ret, ['.'])

    def test_pathsplit_no_slashes(self):
        ret = fileutil.pathsplit('.' + os.path.sep)
        self.assertEqual(ret, ['.'])


class Test_mkdir2(unittest.TestCase):

    @patch('os.makedirs')
    def test_mkdir(self, makedirs_mock):
        kwargs = {'exist_ok': True, 'mode': 511}
        fileutil.mkdir(os.path.join('a', '{b,c}', 'd'), **kwargs)
        self.assertEqual(makedirs_mock.mock_calls, [
            call(os.path.join('a', 'b', 'd'), **kwargs),
            call(os.path.join('a', 'c', 'd'), **kwargs)])

    @patch('os.makedirs')
    def test_mkdir_complicated(self, makedirs_mock):
        kwargs = {'exist_ok': True, 'mode': 511}
        fileutil.mkdir(os.path.join('a', '{b,c}', 'd', '{e,f}'), **kwargs)
        self.assertEqual(makedirs_mock.mock_calls, [
            call(os.path.join('a', 'b', 'd', 'e'), **kwargs),
            call(os.path.join('a', 'b', 'd', 'f'), **kwargs),
            call(os.path.join('a', 'c', 'd', 'e'), **kwargs),
            call(os.path.join('a', 'c', 'd', 'f'), **kwargs)])

    @patch('os.makedirs')
    def test_mkdir_no_expand_paths(self, makedirs_mock):
        kwargs = {'exist_ok': True, 'mode': 511}
        fileutil.mkdir(os.path.join('a', '{b,c}', 'd'), expand_paths=False, **kwargs)
        self.assertEqual(makedirs_mock.mock_calls, [
            call(os.path.join('a', '{b,c}', 'd'), **kwargs),])


    def test_expand_paths(self):
        ret = fileutil._expand_paths('a/b')
        self.assertEqual(ret, ['a/b'])

    def test_expand_paths1(self):
        ret = fileutil._expand_paths('a')
        self.assertEqual(ret, ['a'])

    def test_expand_paths2(self):
        ret = fileutil._expand_paths('{a,b,c}')
        self.assertEqual(ret, ['a', 'b', 'c'])

    def test_expand_paths3(self):
        ret = fileutil._expand_paths('{a,b,c}/d')
        self.assertEqual(ret, ['a/d', 'b/d', 'c/d'])

    def test_expand_paths4(self):
        ret = fileutil._expand_paths('a/{b,c,c}')
        self.assertEqual(ret, ['a/b', 'a/c', 'a/d'])

    def test_expand_paths4(self):
        ret = fileutil._expand_paths('a/{b,c}/d')
        self.assertEqual(ret, ['a/b/d', 'a/c/d'])

    def test_expand_paths4(self):
        ret = fileutil._expand_paths('a/{b,c}/d/{e,f}')
        self.assertEqual(['a/b/d/e', 'a/b/d/f', 'a/c/d/e', 'a/c/d/f'], ret)

    # def test_expand_paths5(self):
    #     ret = fileutil._expand_paths('a{aa,bb}')
    #     self.assertEqual(['aaa', 'abb'], ret)
