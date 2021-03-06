"""
BAse to communicate google drive files

Copyright 2019 Denis Brailovsky, denis.brailovsky@gmail.com

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import os

from open_mlstat.tools.load_drive_files import CONFIGS_STORAGE_ROOT
from open_mlstat.security.google_object_access import ObjectAccess

class GoogleDriveObject(object):

    def __init__(self, service, name, object_type, object_acess, contain_folder="default"):
        """

        :param service:
        :param name:
        :param object_type:
        :type object_acess: ObjectAccess
        :param contain_folder:
        """
        self.contain_folder = contain_folder
        self.name = name
        self.object_type = object_type
        self.service = service
        self.__object_access = object_acess

    def access(self, index):
        self.__object_access.set_roles(index)

    @property
    def config_path(self):
        root = os.path.join(CONFIGS_STORAGE_ROOT, self.contain_folder, self.object_type)
        return os.path.join(root, self.name + ".json")