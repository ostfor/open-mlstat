import os

from open_mlstat.tools import ACCESS_ROOT


class GoogleDriveObject(object):

    def __init__(self, service, name, object_type, contain_folder="default"):
        self.contain_folder = contain_folder
        self.name = name
        self.object_type = object_type
        self.service = service

    def access(self, sid):
        # Dostup
        shareRes = self.service.permissions().create(
            fileId=sid,
            body={'type': 'anyone', 'role': 'reader'},
            fields='id'
        ).execute()
        return shareRes

    @property
    def config_path(self):
        root = os.path.join(ACCESS_ROOT,self.contain_folder, self.object_type)
        return os.path.join(root, self.name + ".json")