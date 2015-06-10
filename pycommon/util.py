def str_or_list_to_list(path_or_paths):
    if isinstance(path_or_paths, str):
        # parameter is a string, turn it into a list of strings
        paths = [path_or_paths]
    else:
        # parameter is a list
        paths = path_or_paths
    return paths
