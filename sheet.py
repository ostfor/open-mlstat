import apiclient.discovery
import httplib2
import json
import os
from oauth2client.service_account import ServiceAccountCredentials

ACCESS_ROOT = "data/access"
ACCESS_SPREAD_SHEET = os.path.join(ACCESS_ROOT, "spread_sheet.json")


def reshape(l):
    return [[e] for e in l]


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

    def prepare_set_values_append(self, range_, value_range_body, value_input_option, insert_data_option):
        #TODO: Test it

        request = self.service.spreadsheets().values().append(spreadsheetId=self.spreadsheetId, range=range_,
                                                              valueInputOption=value_input_option,
                                                              insertDataOption=insert_data_option,
                                                              body=value_range_body)
        response = request.execute()
        return response

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


class GoogleTable(object):

    def __init__(self, CREDENTIALS_FILE='/home/brailovsky/Development/.old/scnn/data/api/drive.json'):
        if not os.path.exists(ACCESS_ROOT):
            os.makedirs(ACCESS_ROOT)

        credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                                       ['https://www.googleapis.com/auth/spreadsheets',
                                                                        'https://www.googleapis.com/auth/drive'])
        self.httpAuth = credentials.authorize(httplib2.Http())
        self.service = apiclient.discovery.build('sheets', 'v4', http=self.httpAuth)
        self.__spreadsheet = None
        self.__access(self.spread_sheet_id)
        self.sheet_element = SheetElement(self.service, "Parameters", self.spread_sheet_id)

    @property
    def spread_sheet_id(self):
        return self.spread_sheet['spreadsheetId']

    @property
    def spread_sheet(self):
        if self.__spreadsheet is None:
            if os.path.exists(ACCESS_SPREAD_SHEET):
                with open(ACCESS_SPREAD_SHEET) as sheet_f:
                    self.__spreadsheet = json.load(sheet_f)
            else:
                self.__spreadsheet = self.create()
                with open(ACCESS_SPREAD_SHEET, 'w') as sheet_f:
                    json.dump(self.__spreadsheet, sheet_f)
        return self.__spreadsheet

    def create(self):
        # Create table
        spreadsheet = self.service.spreadsheets().create(body={
            'properties': {'title': 'NewSpreadSheet', 'locale': 'ru_RU'},
            'sheets': [{'properties': {'sheetType': 'GRID',
                                       'sheetId': 0,
                                       'title': 'Parameters',
                                       'gridProperties': {'rowCount': 2, 'columnCount': 15}}}]
        }).execute()
        return spreadsheet

    def __access(self, sid):
        # Dostup
        driveService = apiclient.discovery.build('drive', 'v3', http=self.httpAuth)
        shareRes = driveService.permissions().create(
            fileId=sid,
            body={'type': 'anyone', 'role': 'reader'},
            fields='id'
        ).execute()
        return shareRes

    def set_title(self):
        titles = ["ID", "Date", "Run_Date", "Epoch", "Loss", "Accuracy", "Model weights Link", "Model configuration",
                  "Model run command", "Commit", "Test Set Link", "Train Set Link", "Statics Snapshots Folder",
                  "Server Name", "Time per epoch"]
        self.sheet_element.prepare_set_values("A1:O1", reshape(titles), "COLUMNS")
        self.sheet_element.run_prepared()


class SheetQuery():
    def __init__(self, start_id=0):
        # TODO: append
        self.__query = [str(start_id)] + [""] * 14

    def prepare_fake_query(self):
        fake_values = ["0", "0", "0", "0.1", "0.9", "http://aaa.aa", "{}", "./run --param 1", "afs55dwgsdg"]
        num = 1
        return [num] + fake_values


if __name__ == '__main__':
    gt = GoogleTable()
    gt.set_title()
