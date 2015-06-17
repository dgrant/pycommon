from six.moves.urllib.parse import urlencode
from six.moves.urllib.request import urlopen

def do_http_get(url, params=None):
    """
    Perform an http get, returning the response data.

    :param url: full url including protocol and port
    :param params: dictionary of parameters
    :return: the body of the HTTP response
    """
    if params is not None:
        url = (url + '?%s') % urlencode(params)
    # print('url=', url)
    url_handle = urlopen(url)
    return url_handle.read().decode('utf8')
