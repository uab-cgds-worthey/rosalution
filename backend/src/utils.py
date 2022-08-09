"""General utilities for the application"""

import random
import re
import string

RELATIVE_FIXUTRE_DIRECTORY_PATH = "../fixtures/"

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
