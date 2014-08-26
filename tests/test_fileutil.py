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
