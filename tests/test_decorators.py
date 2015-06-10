import os
import random
import unittest

from pycommon.decorators import chdir, memoize

@memoize
def memoized_func():
    return random.random()

@memoize
def memoized_func2(arg1, arg2, arg3=None, arg4=None):
    return random.random()


class TestMemoize(unittest.TestCase):

    def test_basic(self):
        first_ret = memoized_func()
        second_ret = memoized_func()

        self.assertEqual(first_ret, second_ret)

    def test_morecomplicated(self):
        first_ret = memoized_func2('a', 'b', arg3='c', arg4=None)
        second_ret = memoized_func2('a', 'b', arg3='c', arg4=None)

        self.assertEqual(first_ret, second_ret)

    def test_morecomplicated2(self):
        first_ret = memoized_func2('a', 'b', arg3='c')
        second_ret = memoized_func2('a', 'b', arg3='c', arg4=None)

        self.assertNotEqual(first_ret, second_ret)

@chdir('test_dir')
def chdir_tester():
    return os.getcwd()

class TestChdir(unittest.TestCase):
    test_dir = os.path.abspath('test_dir')

    def tearDown(self):
        if os.path.exists(self.test_dir):
            os.rmdir(self.test_dir)

    def test_basic(self):
        self.assertNotEqual(os.getcwd(), self.test_dir)
        os.mkdir(self.test_dir)
        self.assertEqual(chdir_tester(), self.test_dir)
        self.assertNotEqual(os.getcwd(), self.test_dir)

    def test_createdir(self):
        self.assertNotEqual(os.getcwd(), self.test_dir)
        self.assertEqual(chdir_tester(), self.test_dir)
        self.assertNotEqual(os.getcwd(), self.test_dir)
        self.assertTrue(os.path.exists(self.test_dir))

