import os
import re

PLOT_FILE_PATH = "../../plots/"

def load_environment():
    environment_variables=["ROSALUTION_BASE_URL", "ROSALUTION_CLIENT_ID", "ROSALUTION_CLIENT_SECRET"]
    config = {env_variable: os.environ.get(env_variable, "default") for env_variable in environment_variables}
    config["ROSALUTION_API_URL"] = f"{config['ROSALUTION_BASE_URL']}/api"
    return config

def plot_filepath():
    """Returns the path to the plots directory"""
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    return os.path.join(current_directory, PLOT_FILE_PATH)

def print_progress(icon: str, message: str, action: str = ""):
    print(f"{icon} {message}...{action}", end="\r", flush=True)


def print_message(icon: str, message: str, action: str = ""):
    print(f"{icon} {message}...{action}", end="\n", flush=True)

def remove_text_in_parentheses(text):
    """Remove any text within parentheses from the text string."""
    return re.sub(r"\([^)]*\)", "", text)