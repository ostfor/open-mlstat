"""
Main tool for saving statistics

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

from open_mlstat.google_sheets.sheet import GoogleTable
from open_mlstat.google_drive.data_loader import DataLoader
from open_mlstat.security.google_object_access import ObjectAccess
from open_mlstat.security.google_account import GoogleAcc


class GoogleDocsStats(object):
    def __init__(self, experiment_name, credentials, who_access='anyone', role='writer'):
        self.experiment_name = experiment_name
        self.__acc = GoogleAcc(credentials)
        self.__object_access = ObjectAccess(self.__acc, who_access=who_access, role=role)

        self.google_table = GoogleTable(self.__acc, self.__object_access, experiment_name)
        self.__acc.drive_service.files().emptyTrash()

    def add(self, query, test_set_file, weights_file=None, train_set_file=None, snapshot=None):
        """
        Add ad stat data to table
        :param query: Query object
        :param test_set_file: path to file or testset name
        :param weights_file: path to weights to upload or just index of weights
        :param train_set_file: path to file or trainset name
        """
        dl = DataLoader(self.__acc, self.__object_access, self.experiment_name, query.run_date, test_set_file)
        query.set_loadable_data(dl, weights=weights_file, test_set=test_set_file,
                                train_set=train_set_file, snapshot=snapshot)
        self.google_table.values_append(query.values)
