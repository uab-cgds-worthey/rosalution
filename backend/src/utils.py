"""General utilities for the application"""

import json
import os

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
