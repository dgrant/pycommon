import _io
from mock import MagicMock

def mock_open(read_data='', lines=None):
    """
    A helper function to create a mock to replace the use of `open`. It works
    for `open` called directly or used as a context manager.

    The `mock` argument is the mock object to configure. If `None` (the
    default) then a `MagicMock` will be created for you, with the API limited
    to methods or attributes available on standard file handles.

    `read_data` is a string for the `read` method of the file handle to return.
    This is an empty string by default.
    """
    file_spec = list(set(dir(_io.TextIOWrapper)).union(set(dir(_io.BytesIO))))

    mock = MagicMock(name='open', spec=open)

    handle = MagicMock(spec=file_spec)
    handle.write.return_value = None
    handle.__enter__.return_value = handle
    handle.read.return_value = read_data

    if lines is not None:
        handle.__iter__.return_value = iter(lines)

    mock.return_value = handle
    return mock
