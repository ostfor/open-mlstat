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
import json, os
from open_mlstat.google_sheets.sheet import GoogleTable
from open_mlstat.google_drive.data_loader import DataLoader
from open_mlstat.security.google_object_access import ObjectAccess
from open_mlstat.security.google_account import GoogleAcc

from open_mlstat.tools.helpers import current_timestamp
from open_mlstat.google_sheets.sheet_query import SheetQuery_1

class GoogleDocsStats(object):
    def __init__(self, config, who_access='anyone', role='writer'):
        assert os.path.exists(config)
        with open(config, 'r') as f:
            config = json.load(f)
        self.experiment_name = config["experiment_name"]
        self.__acc = GoogleAcc(config["credentials"])
        self.__object_access = ObjectAccess(self.__acc, who_access=who_access, role=role)

        self.google_table = GoogleTable(self.__acc, self.__object_access, self.experiment_name,
                                        titles=config["table_titles"])
        self.__acc.drive_service.files().emptyTrash()
        self.__timestamp = current_timestamp()
        self.dl = DataLoader(self.__acc, self.__object_access, self.experiment_name)
        self.query = SheetQuery_1(config["table_titles"],self.dl, self.__timestamp)

    def add(self, query, actions):
        """
        Add ad stat data to table
        :param query: Query object
        :param test_set_file: path to file or testset name
        :param weights_file: path to weights to upload or just index of weights
        :param train_set_file: path to file or trainset name
        """
        self.google_table.values_append(self.query.new(query, actions))
