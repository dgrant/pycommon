import os
import tempfile
import shutil
import unittest
from mock import patch, call, sentinel

from pycommon import testutil
from pycommon import hash

class TestHash(unittest.TestCase):

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()

    def tearDown(self):
        if os.path.exists(self.tempdir):
            shutil.rmtree(self.tempdir)

    def test_it_md5sum(self):
        testfile = os.path.join(self.tempdir, 'blah')
        with open(testfile, 'w') as fp:
            fp.write('a b\nc d\n')
        md5 = hash.md5sum_file(testfile)
        self.assertEqual(md5, '5fea136803bbcf0e1acb97e641bd6ffb')

    def test_it_md5sum_multiple(self):
        testfile1 = os.path.join(self.tempdir, 'blah1')
        testfile2 = os.path.join(self.tempdir, 'blah2')

        with open(testfile1, 'w') as fp:
            fp.write('a b\nc d\n')
        with open(testfile2, 'w') as fp:
            fp.write('e f\n')
        md5 = hash.md5sum_file(self.tempdir)
        self.assertEqual(md5, 'ebcbfa0c9d86a34e449aa706a1ea2fb9')

