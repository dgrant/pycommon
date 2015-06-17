import os
import shutil
import tempfile
import unittest
from mock import patch, call

from pycommon import testutil
from pycommon import csvutil

class TestCsv(unittest.TestCase):

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()

    def tearDown(self):
        if os.path.exists(self.tempdir):
            shutil.rmtree(self.tempdir)

    def test_write_csv_file(self):
        rows = [['a', 'b'], ['c', 'd']]
        filename = os.path.join(self.tempdir, 'test.csv')
        csvutil.write_csv_file(filename, rows)

        contents = open(filename).read()
        self.assertEqual(contents, 'a,b' + os.linesep + 'c,d' + os.linesep)

    def test_write_csv_file_with_header(self):
        rows = [['a', 'b'], ['c', 'd']]
        header = ['head', 'er']
        filename = os.path.join(self.tempdir, 'test.csv')
        csvutil.write_csv_file(filename, rows, header=header)

        contents = open(filename).read()
        self.assertEqual(contents, 'head,er' + os.linesep + 'a,b' + os.linesep + 'c,d' + os.linesep)


    # @patch('csv.writer')
    # def test_write_csv_file_with_header(self, csv_writer_mock):
    #     # Setup
    #     rows = [['a', 'b'], ['c', 'd']]
    #     header = ['head', 'er']
    #     m = testutil.mock_open()
    #     with patch('pycommon.csv.open', m, create=True):
    #         # Call method-under-test
    #         csvutil.write_csv_file('filename', rows, header=header)
    #
    #     # Verification
    #     m.assert_called_with('filename', 'w')
    #     #handle = m.return_value
    #     #csv_writer_mock.assert_called_once_with(handle, delimeter=',')
    #     expected_calls = [call(['head', 'er']), call(['a', 'b']), call(['c', 'd'])]
    #     writer = csv_writer_mock.return_value
    #     self.assertEqual(writer.writerow.call_args_list, expected_calls)
