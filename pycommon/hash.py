import hashlib
import os

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
        if os.path.isdir(filename):
            for file in fileutil.file_iterator(filename):
                _update_md5_sum(file, md5sum)
        else:
            _update_md5_sum(filename, md5sum)

    return md5sum.digest()

def _update_md5_sum(filename, md5sum):
    with open(filename) as file_handle:
        for line in file_handle:
            md5sum.update(line.encode('utf8'))
    return md5sum