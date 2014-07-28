import unittest
from mock import patch, call

from pycommon import testutil
from pycommon import csv

class TestCsv(unittest.TestCase):

    @patch('csv.writer')
    def test_write_csv_file(self, csv_writer_mock):
        rows = [['a', 'b'], ['c', 'd']]
        m = testutil.mock_open()
        with patch('pycommon.csv.open', m, create=True):
            csv.write_csv_file('filename', rows)

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
        m = testutil.mock_open()
        with patch('pycommon.csv.open', m, create=True):
            # Call method-under-test
            csv.write_csv_file('filename', rows, header=header)

        # Verification
        m.assert_called_with('filename', 'w')
        #handle = m.return_value
        #csv_writer_mock.assert_called_once_with(handle, delimeter=',')
        expected_calls = [call(['head', 'er']), call(['a', 'b']), call(['c', 'd'])]
        writer = csv_writer_mock.return_value
        self.assertEqual(writer.writerow.call_args_list, expected_calls)
