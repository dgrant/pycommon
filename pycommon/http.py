from six.moves import urllib

def do_http_get(url, params=None):
    """
    Perform an http get, returning the response data.

    :param url: full url including protocol and port
    :param params: dictionary of parameters
    :return: the body of the HTTP response
    """
    if params is not None:
        url = (url + '?%s') % urllib.parse.urlencode(params)
    # print('url=', url)
    url_handle = urllib.request.urlopen(url)
    return url_handle.read().decode('utf8')
