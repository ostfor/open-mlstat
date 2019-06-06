"""
Element for requesting google sheet

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

class SheetElement:

    def __init__(self, service, sheet_title, spreadsheet_id):

        self.spreadsheetId = spreadsheet_id
        self.service = service
        self.sheetTitle = sheet_title

        self.requests = []
        self.valueRanges = []

    def prepare_set_values(self, cellsRange, values, majorDimension="ROWS"):
        self.valueRanges.append(
            {"range": self.sheetTitle + "!" + cellsRange, "majorDimension": majorDimension, "values": values})



    # spreadsheets.batchUpdate and spreadsheets.values.batchUpdate
    def run_prepared(self, valueInputOption="USER_ENTERED"):
        upd1Res = {'replies': []}
        upd2Res = {'responses': []}
        try:
            if len(self.requests) > 0:
                upd1Res = self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheetId,
                                                                  body={"requests": self.requests}).execute()
            if len(self.valueRanges) > 0:
                upd2Res = self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.spreadsheetId,
                                                                           body={"valueInputOption": valueInputOption,
                                                                                 "data": self.valueRanges}).execute()
        finally:
            self.requests = []
            self.valueRanges = []
        return upd1Res['replies'], upd2Res['responses']