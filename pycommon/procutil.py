import platform
import subprocess

from pycommon import util

def is_linux_or_mac():
    return platform.system() == 'Linux' or platform.system() == 'Darwin'

def kill_process_by_name(procnames):
    procname_list = util.str_or_list_to_list(procnames)
    for procname in procname_list:
        if is_linux_or_mac():
            subprocess.call(['killall', procname])
        else:
            subprocess.call('taskkill /F /IM ' + procname, shell=True)
