"""
Script: genomic_unit_screenshot.py

Description:
This script automates the process of capturing screenshots of web-based genomic data
visualizations. Using Selenium, it navigates to specified urls for different genomic
datasets, and saves the screenshot to a /tmp directory within the current directory.

Usage:
1. Ensure the `.env` file contains the required
    a. `ROSALUTION_CLIENT_ID` & `ROSALUTION_CLIENT_SECRET` for your Rosalution user
    b. `ROSALUTION_API_URL` for the target Rosalution
        ex. https://local.rosalution.cgds/rosalution/api/
2. Provide list of Rosalution analyses to create screen captures for. Important to note, that if
   there are spaces within the name of an analysis, it must be surounded by double or single
   quotes.

Output:
- Screenshots saved in the `tmp/` directory with filenames that follow the pattern:
    `{genomic_unit}-{dataset}-{date}.png`
"""
import contextlib
import csv
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
from datetime import datetime
import urllib3

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.support import expected_conditions as EC

import requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def load_environment():
    environment_variables=["ROSALUTION_BASE_URL", "ROSALUTION_CLIENT_ID", "ROSALUTION_CLIENT_SECRET"]
    config = {env_variable: os.environ.get(env_variable, "default") for env_variable in environment_variables}
    config['ROSALUTION_BASE_URL'] = 'https://local.rosalution.cgds/rosalution'
    config["ROSALUTION_API_URL"] = f"{config['ROSALUTION_BASE_URL']}/api"
    return config


def print_progress(icon: str, message: str, action: str = ""):
    print(f"{icon} {message}...{action}", end="\r", flush=True)


def print_message(icon: str, message: str, action: str = ""):
    print(f"{icon} {message}...{action}", end="\n", flush=True)

class RosalutionAnalysis():
    """
    Representing a Rosalution analysisf for genomic units and annotations,
    and screencaptures datasets to save.
    """

    def __init__(self, analysis_name_string, rosalution_api_url, rosalution_auth_header):
        """Initialize the Rosalution screencapture analyses"""
        self.analysis_name = analysis_name_string
        self.captured_datasets = {}
        self.api_url =rosalution_api_url
        self.auth_header = rosalution_auth_header

    def insert_xenopus_model_system_if_not_exist(self):
        logging_message_base = "Inserting Xenopus Model System into Rosalution MongoDB database via Docker subprocess..."
        print_progress("-", logging_message_base)
        command = ["docker", "compose", "exec", "rosalution-db", "mongosh", "--quiet", "--eval", f"var cpamAnalysis='{self.analysis_name}';var modelSystem='Xenopus Model System'", "/tmp/administration/insert-animal-model-systems.js"]
        try:
            # Execute the command and capture output
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            print_progress("-", logging_message_base, "Success")
            print(result.stdout.rstrip("\n").removesuffix("\n"))
            return

        except subprocess.CalledProcessError as error:
            print_progress("-", logging_message_base, f"Failure with exit code {error.returncode}")
            print(error.stdout.rstrip("\n").removesuffix("\n"))
            print(error.stderr.rstrip("\n").removesuffix("\n"))

    def save_section_changes_batch(self,array: list):
        batch_save_api_url = f"{self.api_url}/analysis/{self.analysis_name}/sections/batch"
        logging_message_base = f"Saving Xenopus Model System Content via Rosalution REST API at {batch_save_api_url}"
        print_progress("+", logging_message_base)
        response = requests.post(batch_save_api_url, headers=self.auth_header, data=json.dumps(array), verify=False, timeout=20)
        result_text = "Success" if response.status_code in [200, 201] else "Failed"
        print_message("+", logging_message_base, result_text)

config = load_environment()
def rosalution_authenticate():
    """Authenticates and returns the request header to authenticate with Rosalution"""

    print_progress("🔒", f"Authenticating with Rosalution at {config['ROSALUTION_BASE_URL']}....")
    client_id, client_secret = (config["ROSALUTION_CLIENT_ID"], config["ROSALUTION_CLIENT_SECRET"])
    auth_headers = {"Content-Type": "application/x-www-form-urlencoded"}
    auth_data = f"client_id={client_id}&client_secret={client_secret}"
    api_auth_token_url = f"{config['ROSALUTION_API_URL']}/auth/token"
    print_message("🔒", f"Requesting Auth from Rosalution at {api_auth_token_url}....")
    auth_response = requests.post(api_auth_token_url, headers=auth_headers, data=auth_data, verify=False, timeout=20)
    auth_response_json = auth_response.json()
    if "access_token" not in auth_response_json:
        print_progress("🔒", "Authenticating with Rosalution", "Failed")
        sys.exit(2)

    print_message("🔒", "Authenticating with Rosalution", "Complete")
    return {
        'Content-Type': 'application/json',
        "Authorization": f"Bearer {auth_response_json['access_token']}"}

def extract_santized_gene_text(gene_column_str: str)->str:
    return re.split(r'[,\s(]+', gene_column_str)[0].upper()

def read_xenopus_tracking_csv_info(csv_file_path: str) -> dict:
    csv_info = {}
    name_simple = ['CPAM0002', 'CPAM0044', 'CPAM0046', 'CPAM0047', 'CPAM0053', 'CPAM0065', 'CPAM0084', 'CPAM0085', 'CPAM0034']

    build_name = lambda cpamid, gene: f"{cpamid} ({gene})"
    with open(csv_file_path, mode='r', encoding='utf-8-sig') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            name = row['case ID']
            row['sanitized_gene'] = extract_santized_gene_text(row['Gene'])
            case_id = name if name in name_simple else build_name(name, row['sanitized_gene'])
            csv_info[case_id] = row

        csv_info['CPAM0034 (KAT6A, USP9X)'] = csv_info['CPAM0034']
        csv_info.pop('CPAM0034')
    return csv_info

xenopus_tracking_csv = sys.argv[1]

rosalution_auth_header = rosalution_authenticate()

print(f"🧬 Extracting Xenopus Projects from '{xenopus_tracking_csv}'...")
xenopus_projects = read_xenopus_tracking_csv_info(xenopus_tracking_csv)

print(*[f"   🐸 {project}" for project in xenopus_projects], sep="\n")

for analysis_name in xenopus_projects:
    print_message("🐸", f"Processing {analysis_name}.......")
    xenopus_model_data = xenopus_projects[analysis_name]
    analysis = RosalutionAnalysis(analysis_name, config['ROSALUTION_API_URL'], rosalution_auth_header)
    analysis.insert_xenopus_model_system_if_not_exist()
    xenopus_section_content = [{
        'header': 'Xenopus Model System',
        'content': [{
            'fieldName': 'Mutation',
            'value': [f'{xenopus_model_data["Gene"]} {xenopus_model_data["variant"]}']
        }, {
            'fieldName': 'Design',
            'value': [xenopus_model_data['cloning']]
        }, {
            'fieldName': 'Diagnoses',
            'value': [xenopus_model_data['phenotype analysis']]
        }]
    }]

    analysis.save_section_changes_batch(xenopus_section_content)

