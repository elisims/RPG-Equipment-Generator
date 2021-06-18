"""
This is the backend module and supports all the REST actions for the
backend
"""

import json
import importlib
import sys

# sys.path.insert(1, './python')

import rand_equip_gen as randomizer
# moduleName = './python/randomizer'
# importlib.import_module(moduleName)


def get_col_exceptions():
    with open('static/json/col_exceptions.json') as f:
        data = json.load(f)
    return data

def get_random_item(item_type=None):
    string = randomizer.return_random_item(item_type)
    return string