import os

from pycommon import util

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
    paths = util.str_or_list_to_list(path_or_paths)

    paths_to_create = []
    if expand_paths:
        for path in paths:
            paths_to_create += _expand_paths(path)
    else:
        paths_to_create = paths

    for path in paths_to_create:
        os.makedirs(path, exist_ok=exist_ok, mode=mode)
