"""
Load data

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

from open_mlstat.google_drive.drive import GoogleDrive
from open_mlstat.tools.zip_data import zip_data
from googleapiclient.errors import HttpError
import logging
from open_mlstat.tools.helpers import current_timestamp


class DataLoader:
    def __init__(self, google_acc, object_access, experiment_name, run_timestamp):
        self.logger = logging.getLogger(__name__)
        self.object_access = object_access
        self.experiment_name = experiment_name
        self.google_acc = google_acc
        self.keywords = {"{run_timestamp}":run_timestamp}
        self.root = GoogleDrive.Folder(self.experiment_name + "_train_statistics", self.google_acc, self.object_access,
                                       contain_folder=self.experiment_name)
        print("Data folder: ", "https://drive.google.com/drive/u/0/folders/" + self.root.id)

    def zip_and_upload_data(self, data_path, save_path,
                            timestemp_prefix=False):
        if data_path is None or not os.path.exists(data_path):
            return data_path
        prefix = None
        if timestemp_prefix:
            prefix = current_timestamp()
        zip_path = zip_data(data_path)
        return self.upload_data(zip_path, save_path, prefix)

    def upload_data(self, data_path, save_path="other", timestemp_prefix=False):
        for k, v in self.keywords.items():
            save_path = save_path.replace(k, v)
        folder_names = save_path.split('/')
        try:
            prefix = None
            if timestemp_prefix:
                prefix = current_timestamp()
            if data_path is None or not os.path.exists(data_path):
                return data_path
            result = "Folder: https://drive.google.com/drive/u/0/folders/{}\nFile id: {}\nFilename: {}"
            curr_dir = self.root
            for folder_name in folder_names:
                curr_dir = GoogleDrive.Folder(folder_name, self.google_acc, self.object_access, curr_dir,
                                              contain_folder=self.experiment_name)
            new_f = GoogleDrive.File(curr_dir, self.google_acc, self.object_access, file_name=data_path, prefix=prefix,
                                     contain_folder=self.experiment_name)
            return result.format(curr_dir.id, new_f.id, new_f.name)
        except HttpError as err:
            self.logger.error("Http Error while upload data %s", err)
            return None
