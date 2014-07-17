"""
A collection of helper functions for the Python standard library or things that access the network or filesystem.
"""

import csv
import functools
import hashlib  # pylint: disable=F0401
import urllib.parse
import urllib.request


def memoize(obj):
    """
    Decorator that caches method calls automagically. Use this decorator on any method and the return values will be
    cached.
    """
    cache = obj.cache = {}

    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        """ The wrapper function """
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = obj(*args, **kwargs)
        return cache[key]
    return memoizer


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


def write_csv_file(filename, rows, header=None):
    """
    Write a list of rows to a CSV file.

    :param filename: pathname of CSV file to write to
    :param rows: a list of rows, each row contains a list of values, each value going in to one column
    :param header: an optional list of column names to go in the header of the CSV file
    :return: nothing
    """
    with open(filename, 'w') as handle:
        writer = csv.writer(handle, delimiter=',')
        if header is not None:
            writer.writerow(header)
        for row in rows:
            writer.writerow(row)


def md5sum_file(filename):
    """
    :param filename: the filename to get the md5 sum of
    :return: the md5 sum of the given filename
    """
    md5sum = hashlib.md5()
    with open(filename) as file_handle:
        for line in file_handle:
            md5sum.update(line.encode('utf8'))
    return md5sum.digest()
