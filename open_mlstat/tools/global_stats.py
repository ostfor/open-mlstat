"""
Main tools

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

from open_mlstat.tools.helpers import current_timestamp, get_addr, get_commit, get_host_name
from open_mlstat.google_sheets.sheet_query import SheetQuery


class GlobalStats(object):
    def __init__(self, run_date, date=None, experiment_name=None, model_config=None, run_command=None, time_epoch=None,
                 test_path=None, train_path=None):
        self.train_path = train_path
        self.test_path = test_path
        self.experiment_name = experiment_name
        if self.experiment_name is None:
            self.experiment_name = "Default"
        self.server_id = get_host_name()
        self.commit = get_commit()

        self.run_date = run_date
        self.time_epoch = time_epoch
        self.run_command = run_command
        self.model_config = model_config
        self.date = date
        if self.date is None:
            self.date = current_timestamp()


def ml_set_statistics(log_statistics, global_stats, epoch, loss, acc, visdom_url, weights_path):
    if log_statistics is not None:
        query = SheetQuery(epoch, epoch, loss, global_stats.run_date,
                           acc, global_stats.date, global_stats.model_config, global_stats.run_command,
                           global_stats.commit, global_stats.server_id, visdom_url
                           )

        log_statistics.add(query, test_set_file=global_stats.test_path, train_set_file=global_stats.train_path,
                           weights_file=weights_path)
    else:
        raise RuntimeWarning("Log statistics is None logging will not be done")
