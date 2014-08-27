import errno
import os
import shutil
import unittest
from mock import patch, call

from pycommon.testutil import mock_open

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


class TestMatchingLineIterator(unittest.TestCase):

    def test(self):
        m = mock_open(lines=['ERROR: line 1', 'WARNING: line 2', 'ERROR: line 3'])
        with patch('pycommon.fileutil.open', m, create=True):
            filtered_lines = list(fileutil.matchingline_iterator('file_name.txt', 'ERROR:.*'))
        self.assertEqual(filtered_lines, ['ERROR: line 1', 'ERROR: line 3'])

class TestFileIterator(unittest.TestCase):
    def setUp(self):
        os.mkdir('temp1')
        os.mkdir('temp1/temp2')
        os.mkdir('temp1/temp2/temp3')
        open('temp1/file1.txt', 'w')
        open('temp1/temp2/file2.txt', 'w')
        open('temp1/temp2/temp3/file3.txt', 'w')
        open('temp1/file4.txt', 'w')

    def tearDown(self):
        shutil.rmtree('temp1')

    def test(self):
        files = list(fileutil.file_iterator('temp1'))

        self.assertEqual(files, ['temp1/file4.txt', 'temp1/file1.txt', 'temp1/temp2/file2.txt', 'temp1/temp2/temp3/file3.txt'])
