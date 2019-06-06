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
import datetime, os

from open_mlstat.google_drive import GoogleDrive


class DataLoader:
    def __init__(self, google_acc, experiment_name, run_date, test_set):
        self.experiment_name = experiment_name
        self.google_acc = google_acc

        self.run_date = str(run_date)
        self.test_set_name = os.path.basename(test_set)
        self.root = GoogleDrive.Folder(self.experiment_name + "_train_statistics", self.google_acc, contain_folder=self.experiment_name)
        print("Data folder: ", "https://drive.google.com/drive/u/0/folders/" + self.root.id)

    def load_data(self, data_path, container_name="weights", prefix=None, levels=("test_set", "container_name",
                                                                                  "experiment_date")):
        if data_path is None or not os.path.exists(data_path):
            return None
        result = "Folder: https://drive.google.com/drive/u/0/folders/{}\nFile id: {}\nFilename: {}"
        curr_dir = self.root

        if "test_set" in levels:
            curr_dir = GoogleDrive.Folder(self.test_set_name, self.google_acc, curr_dir, contain_folder=self.experiment_name)
            if "container_name" in levels:
                curr_dir = GoogleDrive.Folder(container_name, self.google_acc, curr_dir, contain_folder=self.experiment_name)
                if "experiment_date" in levels:
                    curr_dir = GoogleDrive.Folder(self.run_date, self.google_acc, curr_dir, contain_folder=self.experiment_name)

        new_f = GoogleDrive.File(curr_dir, self.google_acc, data_path, prefix=prefix, contain_folder=self.experiment_name)
        return result.format(curr_dir.id, new_f.id, new_f.name)


class SheetQuery(object):
    def __init__(self, idx, epoch, loss, run_date, accuracy=None, date=None,
                 model_config=None, run_command=None, commit=None,
                 server_id=None, time_epoch=None):

        self.__empty_field = "<empty>"
        self.__date = date
        if self.__date is None:
            self.__date = datetime.datetime.now().strftime("%y%m%d_%H%M")

        self.weights_pos = 6
        self.testset_pos = 10
        self.trainset_pos = 11
        self.snapshot_pos = 12


        self.__query = [idx, date, run_date, epoch, loss, accuracy, None, model_config, run_command,
                        commit, None, None, None, server_id, time_epoch]

        self.run_date = self.__query[2]


    def prepare_fake_query(self):
        fake_values = ["0", "0", "0", "0.1", "0.9", "http://aaa.aa", "{}", "./run --param 1", "afs55dwgsdg"]
        num = 1
        return [num] + fake_values

    @property
    def values(self):
        query = [str(q) if q is not None else self.__empty_field for q in self.__query]
        return [query]

    def set_loadable_data(self, dataloader, test_set=None, train_set=None, weights=None,
                          snapshot=None):
        weights_link = dataloader.load_data(weights, "weights", prefix=self.__date)
        testset_link = dataloader.load_data(test_set, "testset", levels=("test_set", "container_name"))
        trainset_link = dataloader.load_data(train_set, "trainset", levels=("test_set", "container_name"))
        snapshot_link = dataloader.load_data(snapshot, "snapshots", prefix=self.__date)

        self.__query[self.weights_pos] = weights_link
        self.__query[self.testset_pos] = testset_link
        self.__query[self.trainset_pos] = trainset_link
        self.__query[self.snapshot_pos] = snapshot_link


if __name__ == '__main__':
    print(SheetQuery(0, 10, 0.6,"060519").values)
