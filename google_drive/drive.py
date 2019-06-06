"""
Creating editing files and folders for googledoc

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
from apiclient.http import MediaFileUpload

from google_drive.drive_object_base import GoogleDriveObject
from tools import get_object

from security.google_account import GoogleAcc

MIMETYPE_FILE = "application/vnd.google-apps.file"
MIMETYPE_PHOTO = "application/vnd.google-apps.photo"
MIMETYPE_DOC = "application/vnd.google-apps.document"
MIME_TYPE_FOLDER = 'application/vnd.google-apps.folder'
MIMETYPE_UNKNOWN = "application/vnd.google-apps.unknown"


class GoogleDrive(object):
    class File(GoogleDriveObject):

        def __init__(self, folder, google_acc, file_name="data/test.txt", mimetype="*/*", prefix=None, contain_folder="default"):
            self.mimetype = mimetype
            self.file_name =file_name
            name = os.path.basename(file_name)

            if prefix is not None:
                name = prefix + "_" + name

            GoogleDriveObject.__init__(self, google_acc.drive_service, name, "files", contain_folder=contain_folder)

            self.file_metadata = {
                'name': self.name,
                'mimeType': self.mimetype,
                'parents': [folder.id]
            }


            self.data = get_object(self.config_path, self.create_file)

            self.id = self.data.get('id')
            self.access(self.id)



        def create_file(self):
            media = MediaFileUpload(self.file_name,
                                    mimetype=self.mimetype,
                                    resumable=True)
            print("Create: ", self.file_metadata)
            return self.service.files().create(body=self.file_metadata,
                                               media_body=media, fields='id').execute()

    class Folder(GoogleDriveObject):
        def __init__(self, name, google_acc, parent=None, contain_folder="default"):
            GoogleDriveObject.__init__(self, google_acc.drive_service, name, "folders", contain_folder=contain_folder)

            self.file_metadata = {
                'name': name,
                'mimeType': MIME_TYPE_FOLDER
            }
            if parent is not None:
                self.file_metadata["parents"] = [parent.id]

            self.data = get_object(self.config_path, self.create_folder)

            self.id = self.data.get('id')
            self.access(self.id)

        def create_folder(self):
            return self.service.files().create(body=self.file_metadata, fields='id').execute()

    def __init__(self, google_acc):
        # Setup the Drive v3 API
        self.google_acc = google_acc

    def create_folder(self, name='root'):
        fold = self.Folder(name, self.google_acc)
        print(fold.id)


if __name__ == '__main__':
    acc = GoogleAcc()
    folder = GoogleDrive.Folder("train_statistics", acc)
    file = GoogleDrive.File(folder, acc)
    print(file.id)
