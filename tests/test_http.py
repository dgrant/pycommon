import collections
import unittest
from mock import patch

from pycommon import http

class TestHttp(unittest.TestCase):

    @patch('six.moves.urllib.request.urlopen')
    def test_do_http_get(self, urlopen_mock):
        # setup
        url = 'http://www.google.ca'
        http_response_string = 'response'
        urlopen_mock.return_value.read.return_value.decode.return_value = http_response_string

        # call method-under-test
        ret = http.do_http_get(url)

        # verify
        urlopen_mock.assert_called_once_with(url)
        urlopen_mock.return_value.read.return_value.decode.assert_called_once_with('utf8')
        self.assertEqual(ret, http_response_string)

    @patch('six.moves.urllib.request.urlopen')
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
        ret = http.do_http_get(url, params)

        # verify
        urlopen_mock.assert_called_once_with(url + "?a=1&b=2&c=3")
        urlopen_mock.return_value.read.return_value.decode.assert_called_once_with('utf8')
        self.assertEqual(ret, http_response_string)
