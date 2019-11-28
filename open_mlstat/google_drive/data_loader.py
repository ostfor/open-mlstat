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


class DataLoader:

    def __init__(self, google_acc, object_access, experiment_name, run_date, test_set):
        self.logger = logging.getLogger(__name__)
        self.object_access = object_access
        self.experiment_name = experiment_name
        self.google_acc = google_acc

        self.run_date = str(run_date)
        self.test_set_name = os.path.basename(test_set)
        self.root = GoogleDrive.Folder(self.experiment_name + "_train_statistics", self.google_acc, self.object_access,
                                       contain_folder=self.experiment_name)
        print("Data folder: ", "https://drive.google.com/drive/u/0/folders/" + self.root.id)

    def zip_and_upload_data(self, data_path, container_name,
                            prefix=None, levels=("test_set", "container_name", "experiment_date")):
        if data_path is None or not os.path.exists(data_path):
            return data_path
        zip_path = zip_data(data_path)
        return self.upload_data(zip_path, container_name, prefix, levels)

    def upload_data(self, data_path, container_name, prefix=None, levels=("test_set", "container_name",
                                                                          "experiment_date")):
        try:
            if data_path is None or not os.path.exists(data_path):
                return data_path
            result = "Folder: https://drive.google.com/drive/u/0/folders/{}\nFile id: {}\nFilename: {}"
            curr_dir = self.root

            if "test_set" in levels:
                curr_dir = GoogleDrive.Folder(self.test_set_name, self.google_acc, self.object_access, curr_dir,
                                              contain_folder=self.experiment_name)
                if "container_name" in levels:
                    curr_dir = GoogleDrive.Folder(container_name, self.google_acc, self.object_access, curr_dir,
                                                  contain_folder=self.experiment_name)
                    if "experiment_date" in levels:
                        curr_dir = GoogleDrive.Folder(self.run_date, self.google_acc, self.object_access, curr_dir,
                                                      contain_folder=self.experiment_name)

            new_f = GoogleDrive.File(curr_dir, self.google_acc, self.object_access, file_name=data_path, prefix=prefix,
                                     contain_folder=self.experiment_name)
            return result.format(curr_dir.id, new_f.id, new_f.name)
        except HttpError as err:
            self.logger.error("Http Error while upload data %s", err)
            return None
