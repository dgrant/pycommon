import hashlib

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
