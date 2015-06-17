import collections
import unittest
from mock import patch

from pycommon import http

class TestHttp(unittest.TestCase):

    def test_it_do_http(self):
        url = 'http://www.google.com'

        ret = http.do_http_get(url)


    def test_it_do_http_get(self):
        url = 'http://www.cnn.com/search'
        params = {'q': 'aabbcc'}

        http.do_http_get(url, params=params)
