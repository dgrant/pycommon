import _io
import collections
import unittest
from mock import patch, call, sentinel

from pycommon import testutil
from pycommon import hash

class TestHash(unittest.TestCase):

    @patch('hashlib.md5')
    def test_md5sum_file(self, md5_mock):
        # Setup
        m = testutil.mock_open(lines=['a', 'b'])
        md5_instance = md5_mock.return_value
        md5_instance.digest.return_value = sentinel.digest
        with patch('builtins.open', m, create=True):
            # Call method-under-test
            digest = hash.md5sum_file('filename')

        # Verification
        m.assert_called_once_with('filename')
        self.assertEqual(md5_instance.update.mock_calls,
                         [call('a'.encode('utf8')), call('b'.encode('utf8'))])
        self.assertEqual(digest, sentinel.digest)


