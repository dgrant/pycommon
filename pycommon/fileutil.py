import errno
import os
import re
import six
import shutil
import tempfile

from pycommon import util

def delete(path_or_paths):
    """
    Delete the provided path (or list of paths). A path can either be a directory or a file.

    :param path_or_paths:
    :return:
    """
    paths = util.str_or_list_to_list(path_or_paths)

    for path in paths:
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
        except OSError as e:
            if e.errno == errno.ENOENT:
                # Ignore case where file/folder doesn't exist
                pass
            else:
                # Re-raise exception
                raise


def mkdir(path_or_paths, mode=0o777, exist_ok=True):
    """
    Slight variation of os.makedirs. exist_ok is True by default. And it accepts a list of paths as input.

    :param path_or_paths: a path or a list of paths
    :param mode: file mode (default is 777)
    :param exist_ok: True (default) if you don't want this function to complain in a directory already exists
    :return:
    """
    paths = util.str_or_list_to_list(path_or_paths)

    for path in paths:
        if six.PY2:
            try:
                os.makedirs(path)
            except OSError as exc: # Python >2.5
                if exc.errno == errno.EEXIST and os.path.isdir(path):
                    pass
                else:
                    raise
        elif six.PY3:
            os.makedirs(path, mode=mode, exist_ok=exist_ok)

def replace_in_file(path, search_str, repl_str, encoding=None):
    """
    Replace a string in a file.

    :param path: the path to replace string in
    :param search_str: the string to find
    :param repl_str: the string to replace
    :return: nothing
    """
    if six.PY2:
        with open(path, 'r') as fp:
            lines = fp.readlines()
    elif six.PY3:
        with open(path, 'r', encoding=encoding) as fp:
            lines = fp.readlines()

    # Write to a temp file, the original lines and any lines that have changed
    (temp_file_handle, temp_file_name) = tempfile.mkstemp()
    try:
        with os.fdopen(temp_file_handle, 'w') as fp:
            for line in lines:
                loc = line.find(search_str)
                while loc != -1:
                    line = line[:loc] + repl_str + line[(loc + len(search_str)):]
                    loc = line.find(search_str)
                fp.write(line)

        # replace the original file with the temp
        delete(path)
        os.rename(temp_file_name, path)
    finally:
        delete(temp_file_name)



def file_iterator(path='.', ext=None):
    """
    Iterate over all files in the specified path with the specified
    extension

    example:
        for path in file_iterator(r'c:\windows', '.dll'):
            print path
    """
    if os.path.isfile(path):
        yield path
        return

    for root, _, files in os.walk(path):
        for _file in files:
            if ext == None or os.path.splitext(_file)[1].lower() == ext:
                yield os.path.join(root, _file)

def matchingline_iterator(path, regex_pat):
    """
    Iterate over lines in the specified file path matching the specified
    regex pattern.

    example:
        for line in matchingline_iterator(r'c:\log.txt', '.*ERROR:.*'):
            print line
    """
    obj = re.compile(regex_pat)
    for line in open(path):
        match_obj = obj.search(line)
        if match_obj is not None:
            yield line
