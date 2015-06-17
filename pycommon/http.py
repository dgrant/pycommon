from six.moves.urllib.parse import urlencode
from six.moves.urllib.request import urlopen
import codecs

def do_http_get(url, params=None):
    """
    Perform an http get, returning the response data.

    :param url: full url including protocol and port
    :param params: dictionary of parameters
    :return: the body of the HTTP response
    """
    if params is not None:
        url = (url + '?%s') % urlencode(params)
    url_handle = urlopen(url)
    return codecs.decode(url_handle.read(), 'utf8', 'ignore')
