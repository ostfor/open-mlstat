"""
Query for google sheet

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
from open_mlstat.tools.helpers import current_timestamp


class SheetQuery_1(object):
    def __init__(self, titles, dataloader, run_timestamp=None):
        self.run_timestamp = run_timestamp
        self.actions = {
            "upload_zip": dataloader.zip_and_upload_data,
            "upload_file": dataloader.upload_data,
            "timestamp": current_timestamp,
            "run_timestamp": self.get_run_timestamp
        }
        self.titles = titles
        self.__empty_field = "<empty>"

    def get_run_timestamp(self):
        return self.run_timestamp

    def new(self, insert_query, actions=None, titles=None):

        if actions is None:
            actions = {}

        if titles is None:
            titles = self.titles

        inserters = []
        insert_data = []

        for k in titles:
            if k not in insert_query.keys():
                inserters.append(None)
                insert_data.append(None)
            else:
                insert_data.append(insert_query[k])
                action = {"action": None}
                if k in actions.keys():
                    action = actions[k]
                if action["action"] is None:
                    inserters.append(None)
                else:
                    inserters.append(action)
        assert len(inserters) == len(insert_data)
        query = []
        for inserter, data in zip(inserters, insert_data):
            _data = data
            if inserter is not None:
                vargs = []
                kargs = {}
                if data is not None:
                    vargs.append(data)
                if "args" in inserter.keys() and inserter["args"] is not None:
                    if type(inserter["args"]) == dict:
                        kargs = inserter["args"]
                    elif type(inserter["args"]) == list:
                        vargs += inserter["args"]
                _data = self.actions[inserter["action"]](*vargs, **kargs)
            query.append(_data)
        print(query)
        return self.__qvalues(query)

    def __qvalues(self, query):
        query = [str(q) if q is not None else self.__empty_field for q in query]
        return [query]
