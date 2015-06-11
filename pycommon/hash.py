import hashlib

from pycommon import util
from pycommon import fileutil

def md5sum_file(filename):
    """
    :param filename: the filename to get the md5 sum of
    :return: the md5 sum of the given filename
    """
    filenames = util.str_or_list_to_list(filename)
    md5sum = hashlib.md5()
    for filename in filenames:
        # Need to turn the iternator into a list and then sort, to ensure that we get the same ordering of files
        # all platforms.
        files = [file for file in fileutil.file_iterator(filename)]
        files.sort()
        for file in files:
            _update_md5_sum(file, md5sum)
    return md5sum.hexdigest()

def _update_md5_sum(filename, md5sum):
    with open(filename) as file_handle:
        for line in file_handle:
            md5sum.update(line.encode('utf8'))
    return md5sum
