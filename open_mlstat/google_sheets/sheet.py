"""
Tool for creating and editing google table

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

from __future__ import print_function
import os, string

from open_mlstat.google_sheets.sheet_element import SheetElement

from open_mlstat.tools import reshape, ACCESS_ROOT, get_object



DEFAULT_TITLES = ("ID", "Date", "Run_Date", "Epoch", "Loss", "Accuracy", "Model weights Link", "Model configuration",
                  "Model run command", "Commit", "Test Set Link", "Train Set Link", "Statistics Snapshots Folder",
                  "Server Name", "Time per epoch", "Visdom / Tensorboard Link")


class GoogleTable(object):

    def __init__(self, google_acc, object_access, scope_name, titles=DEFAULT_TITLES):
        """
        Create google table
        :type google_acc: GoogleAcc
        :param titles: list of titles
        """
        self.object_access = object_access
        self.scope_name = scope_name
        self.titles = titles

        if len(titles) <= len(string.ascii_uppercase):
            self.columns_range = "A1:{}1".format(string.ascii_uppercase[len(titles) - 1])
        else:
            raise NotImplementedError(
                "Number of titles more then {} is not supported yet".format(len(string.ascii_uppercase)))

        if not os.path.exists(ACCESS_ROOT):
            os.makedirs(ACCESS_ROOT)
        self.google_acc = google_acc

        self.__spreadsheet = get_object(os.path.join(ACCESS_ROOT, self.scope_name, "spread_sheet.json"), self.create)

        self.object_access.set_roles(self.spread_sheet_id)
        self.__set_titles()

        print("Table: ", "https://docs.google.com/spreadsheets/d/" + self.spread_sheet_id)

    @property
    def spread_sheet_id(self):
        return self.__spreadsheet['spreadsheetId']

    def create(self):
        # Create table
        spreadsheet = self.google_acc.sheet_service.spreadsheets().create(body={
            'properties': {'title': 'Statistics', 'locale': 'ru_RU'},
            'sheets': [{'properties': {'sheetType': 'GRID',
                                       'sheetId': 0,
                                       'title': self.scope_name,
                                       'gridProperties': {'rowCount': 2, 'columnCount': len(self.titles)}}}]
        }).execute()
        return spreadsheet

    def values_append(self, value_range_body, column_range=None, valueInputOption ="USER_ENTERED"):
        if column_range is None:
            column_range = self.columns_range
        request = self.google_acc.sheet_service.spreadsheets().values().append(
            spreadsheetId=self.spread_sheet_id, range=column_range, valueInputOption=valueInputOption,
            body={"values": value_range_body})
        return request.execute()

    def __set_titles(self):
        sheet_element = SheetElement(self.google_acc.sheet_service, self.scope_name, self.spread_sheet_id)
        sheet_element.prepare_set_values(self.columns_range, reshape(self.titles), "COLUMNS")
        sheet_element.run_prepared()
