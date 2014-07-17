import _io
import collections
import unittest
from mock import patch, Mock, call, MagicMock, sentinel

import pycommon

def mock_open(mock=None, read_data='', lines=None):
    """
    A helper function to create a mock to replace the use of `open`. It works
    for `open` called directly or used as a context manager.

    The `mock` argument is the mock object to configure. If `None` (the
    default) then a `MagicMock` will be created for you, with the API limited
    to methods or attributes available on standard file handles.

    `read_data` is a string for the `read` method of the file handle to return.
    This is an empty string by default.
    """
    file_spec = list(set(dir(_io.TextIOWrapper)).union(set(dir(_io.BytesIO))))

    mock = MagicMock(name='open', spec=open)

    handle = MagicMock(spec=file_spec)
    handle.write.return_value = None
    handle.__enter__.return_value = handle
    handle.read.return_value = read_data

    if lines is not None:
        handle.__iter__.return_value = iter(lines)

    mock.return_value = handle
    return mock

class TestLowLevel(unittest.TestCase):

    @patch('urllib.request.urlopen')
    def test_do_http_get(self, urlopen_mock):
        # setup
        url = 'http://www.google.ca'
        http_response_string = 'response'
        urlopen_mock.return_value.read.return_value.decode.return_value = http_response_string

        # call method-under-test
        ret = pycommon.do_http_get(url)

        # verify
        urlopen_mock.assert_called_once_with(url)
        urlopen_mock.return_value.read.return_value.decode.assert_called_once_with('utf8')
        self.assertEqual(ret, http_response_string)

    @patch('urllib.request.urlopen')
    def test_do_http_get_with_params(self, urlopen_mock):
        # setup
        url = 'http://www.google.ca'
        http_response_string = 'response'
        params = collections.OrderedDict()
        params['a'] = 1
        params['b'] = 2
        params['c'] = 3
        urlopen_mock.return_value.read.return_value.decode.return_value = http_response_string

        # call method-under-test
        ret = pycommon.do_http_get(url, params)

        # verify
        urlopen_mock.assert_called_once_with(url + "?a=1&b=2&c=3")
        urlopen_mock.return_value.read.return_value.decode.assert_called_once_with('utf8')
        self.assertEqual(ret, http_response_string)

    @patch('csv.writer')
    def test_write_csv_file(self, csv_writer_mock):
        rows = [['a', 'b'], ['c', 'd']]
        m = mock_open()
        with patch('pycommon.open', m, create=True):
            pycommon.write_csv_file('filename', rows)

            m.assert_called_with('filename', 'w')
            #handle = m()
            #csv_writer_mock.assert_called_once_with(handle, delimeter=',')
            expected_calls = [call(['a', 'b']), call(['c', 'd'])]
            writer = csv_writer_mock.return_value
            self.assertEqual(writer.writerow.call_args_list, expected_calls)

    @patch('csv.writer')
    def test_write_csv_file_with_header(self, csv_writer_mock):
        # Setup
        rows = [['a', 'b'], ['c', 'd']]
        header = ['head', 'er']
        m = mock_open()
        with patch('pycommon.open', m, create=True):
            # Call method-under-test
            pycommon.write_csv_file('filename', rows, header=header)

        # Verification
        m.assert_called_with('filename', 'w')
        #handle = m.return_value
        #csv_writer_mock.assert_called_once_with(handle, delimeter=',')
        expected_calls = [call(['head', 'er']), call(['a', 'b']), call(['c', 'd'])]
        writer = csv_writer_mock.return_value
        self.assertEqual(writer.writerow.call_args_list, expected_calls)

    @patch('hashlib.md5')
    def test_md5sum_file(self, md5_mock):
        # Setup
        m = mock_open(lines=['a', 'b'])
        md5_instance = md5_mock.return_value
        md5_instance.digest.return_value = sentinel.digest
        with patch('builtins.open', m, create=True):
            # Call method-under-test
            digest = pycommon.md5sum_file('filename')

        # Verification
        m.assert_called_once_with('filename')
        self.assertEqual(md5_instance.update.mock_calls,
                         [call('a'.encode('utf8')), call('b'.encode('utf8'))])
        self.assertEqual(digest, sentinel.digest)


