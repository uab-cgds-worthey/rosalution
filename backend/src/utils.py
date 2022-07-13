"""General utilities for the application"""

import json
import os
import random
import re
import string

from isort import file

RELATIVE_FIXUTRE_DIRECTORY_PATH = "../fixtures/"

def read_fixture(fixture_filename):
    """reads the JSON from the filepath relative to the src directory"""
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    path_to_file = os.path.join(current_directory, RELATIVE_FIXUTRE_DIRECTORY_PATH + fixture_filename)
    with open(path_to_file, mode="r", encoding="utf-8") as file_to_open:
        data = json.load(file_to_open)
        file_to_open.close()

    return data

def write_fixture(fixture_filename, data_to_write):
    """reads the JSON from the filepath relative to the src directory"""
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    path_to_file = os.path.join(current_directory, RELATIVE_FIXUTRE_DIRECTORY_PATH + fixture_filename)
    with open(path_to_file, mode="w", encoding="utf-8") as file_to_write:
        json.dump(data_to_write, file_to_write, ensure_ascii=False, indent=4)

        file_to_write.close()

    # print(type(data_to_write))

    return

def replace(var_string, dataset):
    """ Replaces variables that are encased in {} """
    replace_variables = re.findall(r'\{(.*?)\}', var_string)

    fetched_vars = {}
    for var in replace_variables:
        fetched_vars[var] = dataset[var]

    replaced_str = str.format(**fetched_vars)

    return replaced_str

def randomword():
    """ Temporary function for creating UUIDs that would be made from mongo """
    letters_numbers = string.ascii_letters + string.digits
    return ''.join(random.SystemRandom().choice(letters_numbers) for _ in range(26))
