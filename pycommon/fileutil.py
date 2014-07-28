import errno
import os
import re
import shutil
import tempfile

def str_or_list_to_list(path_or_paths):
    if isinstance(path_or_paths, str):
        # parameter is a string, turn it into a list of strings
        paths = [path_or_paths]
    else:
        # parameter is a list
        paths = path_or_paths
    return paths

def delete(path_or_paths):
    """
    Delete the provided path (or list of paths). A path can either be a directory or a file.

    :param path_or_paths:
    :return:
    """
    paths = str_or_list_to_list(path_or_paths)

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


def pathsplit(path):
    """
    Split a path into a list of directories making up the path. eg. '/usr/share/src' -> ['usr', 'share', 'src']

    :param path: a file path
    :return: a list of path components
    """
    ret = []
    head, tail = os.path.split(path)
    if not tail:
        head, tail = os.path.split(head)
    while tail:
        ret.append(tail)
        head, tail = os.path.split(head)
    ret.reverse()
    return ret

def _expand_paths(path):
    paths = ['']

    for i, path_component in enumerate(pathsplit(path)):
        if path_component[0] == '{' and path_component[-1] == '}':
            branches = path_component[1:-1].split(',')
        else:
            branches = path_component
        new_paths = []
        for path in paths:
            for branch in branches:
                new_paths.append(os.path.join(path, branch))
        paths = new_paths

    return paths

def mkdir(path_or_paths, expand_paths=True, mode=0o777, exist_ok=True):
    paths = str_or_list_to_list(path_or_paths)

    paths_to_create = []
    if expand_paths:
        for path in paths:
            paths_to_create += _expand_paths(path)
    else:
        paths_to_create = paths

    for path in paths_to_create:
        os.makedirs(path, exist_ok=exist_ok, mode=mode)

def replace_in_file(path, search_str, repl_str, encoding=None):
    """
    BETA

    Replace a string in a file.

    :param path: the path to replace string in
    :param search_str: the string to find
    :param repl_str: the string to replace
    :return: nothing
    """
    with open(path, 'r', newline='', encoding=encoding) as fp:
        lines = fp.readlines()

    try:
        # Write to a temp file, the original lines and any lines that have changed
        (temp_file_handle, temp_file_name) = tempfile.mkstemp()
        with os.fdopen(temp_file_handle, 'w') as fp:
            for line in lines:
                loc = line.find(search_str)
                if loc != -1:
                    line = line[:loc] + repl_str + line[(loc + search_str):]
                fp.write(line)

        # replace the original file with the temp
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
        match_obj = obj.search(regex_pat)
        if match_obj is not None:
            yield line
