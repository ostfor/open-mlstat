"""
Helping tools

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


import json
import os


CONFIGS_STORAGE_ROOT = "data/files"


def load_object_by_config(path_cfg, get_method):
    """
    Read configuration by objects (file/folder) name or create a new if it not exists
    :param path_cfg: path to configuration
    :param get_method:
    :return:
    """
    if os.path.exists(path_cfg):
        with open(path_cfg) as sheet_f:
            data = json.load(sheet_f)
    else:
        root = os.path.dirname(path_cfg)
        if not os.path.exists(root):
            os.makedirs(root)
        data = get_method()
        with open(path_cfg, 'w') as sheet_f:
            json.dump(data, sheet_f)
    return data
