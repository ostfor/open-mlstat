import getpass
import socket

import git


def get_commit():
    repo = git.Repo(search_parent_directories=True)
    sha = repo.head.object.hexsha
    return sha


def get_host_name():
    hostname = socket.gethostname()
    username = getpass.getuser()
    return username + "_" + hostname