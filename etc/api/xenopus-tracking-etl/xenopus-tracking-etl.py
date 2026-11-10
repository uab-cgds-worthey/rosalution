"""
Script: xenopus-tracking-etl.py

Description:
Processes UTF-8 CSV exports from Microsoft Excel Xenopus Tracking Progress spreadsheet.
For each analysis in the spreadsheet, the script identifies if the 'Xenopus Model System'
section has been inserted into the Rosalution analysis and reports to std out if not.
When the 'Xenopus Model System' section exists the script updates the section with the
data from the spreadsheet.

Important note:
Updates to an existing 'Xenopus Model System' section overwrite the values in the
following fields:
- Mutation
- Design
- Diagnoses

Usage:
1. Ensure shell has the following environment variables set with the Rosalution
   REST API credentials
    a. `ROSALUTION_CLIENT_ID` & `ROSALUTION_CLIENT_SECRET` for your Rosalution user
    b. `ROSALUTION_API_URL` for the target Rosalution
        ex. https://local.rosalution.cgds/rosalution/api/
2. Provide the exported UTF-8 CSV page from the excel spreadsheet as a script argument

Output:
- Updates 'Xenopus Model System' sections in Rosalution with data from the spreadsheet.
- Prints a list of analyses missing the 'Xenopus Model System' section and require
  require the `etc/administration/insert-animal-model-systems.js` script to be run.
"""
import csv
import json
import os
import re
import subprocess
import sys
import urllib3

import requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def load_environment():
    environment_variables=["ROSALUTION_BASE_URL", "ROSALUTION_CLIENT_ID", "ROSALUTION_CLIENT_SECRET"]
    config = {env_variable: os.environ.get(env_variable, "default") for env_variable in environment_variables}
    config["ROSALUTION_API_URL"] = f"{config['ROSALUTION_BASE_URL']}/api"
    return config


def print_progress(icon: str, message: str, action: str = ""):
    print(f"{icon} {message}...{action}", end="\r", flush=True)


def print_message(icon: str, message: str, action: str = ""):
    print(f"{icon} {message}...{action}", end="\n", flush=True)

class RosalutionAnalysis():
    """
    Representing a Rosalution analysis and provides operations for managing Xenopus Model System content
    using the Rosalution REST API.
    """

    def __init__(self, analysis_name_string, rosalution_api_url, rosalution_auth_header):
        """Initialize the Rosalution analysis"""
        self.analysis_name = analysis_name_string
        self.captured_datasets = {}
        self.api_url =rosalution_api_url
        self.auth_header = rosalution_auth_header

    def xenopus_model_system_section_exists(self):
        """
        Queries Rosalution REST API to determine if the 'Xenopus Model System' section exists in the analysis.
        """
        get_analysis_url = f"{self.api_url}/analysis/{self.analysis_name}"
        logging_message_base = f"Querying if 'Xenopus Model System' section exists in {analysis_name}"
        print_progress("+", logging_message_base)
        response = requests.get(get_analysis_url, headers=self.auth_header, verify=False, timeout=20)
        result = response.json()
        for section in result['sections']:
            if section['header'] == 'Xenopus Model System':
                print_message("+", logging_message_base, "Found")
                return True

        print_message("+", logging_message_base, "Not Found")
        return False

    def insert_xenopus_model_system_if_not_exist(self, docker_container_name):
        """
        Insert a 'Xenopus Model System' section into the Rosalution analysis using the MongoDB 
        administration 'insert-animal-model-systems.js' MongoDB shell script. Rosalution's
        MongoDB database in a docker container must be on the same host machine.
        """
        logging_message_base = "Inserting 'Xenopus Model System' into Rosalution via Docker exec subprocess..."
        print_progress("-", logging_message_base)
        script_args= f"var cpamAnalysis='{self.analysis_name}';var modelSystem='Xenopus Model System'"
        script_name="/tmp/administration/insert-animal-model-systems.js"
        command = ["docker", "exec", docker_container_name, "mongosh", "--quiet", "--eval", script_args, script_name]
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            print_message("-", logging_message_base, "Success")
            print(result.stdout.rstrip("\n").removesuffix("\n"))
            return

        except subprocess.CalledProcessError as error:
            print_message("-", logging_message_base, f"Failure with exit code {error.returncode}")
            print(error.stdout.rstrip("\n").removesuffix("\n"))
            print(error.stderr.rstrip("\n").removesuffix("\n"))

    def save_section_changes_batch(self,array: list):
        """Save 'Xenopus Model System' section updates to a Rosalution analysis."""
        batch_save_api_url = f"{self.api_url}/analysis/{self.analysis_name}/sections/batch"
        logging_message_base = f"Saving Batch Section Updates to Rosalution analysis '{self.analysis_name}'"
        print_progress("+", logging_message_base)
        response = requests.post(
            batch_save_api_url, headers=self.auth_header, data=json.dumps(array), verify=False, timeout=20
        )
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
    """Extracts the gene symbol from the 'Gene' column of the spreadsheet """
    return re.split(r'[,\s(]+', gene_column_str)[0].upper()

def read_xenopus_tracking_csv_info(csv_file_path: str) -> dict:
    """Reads the CSV file and returns each row as a value within a dict, where the key is the analysis name"""
    csv_info = {}
    name_simple = [
        'CPAM0002', 'CPAM0044', 'CPAM0046', 'CPAM0047', 'CPAM0053', 'CPAM0065', 'CPAM0084', 'CPAM0085', 'CPAM0034'
    ]

    build_name = lambda cpamid, gene: f"{cpamid} ({gene})"
    with open(csv_file_path, mode='r', encoding='utf-8-sig') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            name = row['case ID']
            row['sanitized_gene'] = extract_santized_gene_text(row['Gene'])
            case_id = name if name in name_simple else build_name(name, row['sanitized_gene'])
            csv_info[case_id] = row
        if 'CPAM0034' in csv_info:
            csv_info['CPAM0034 (KAT6A, USP9X)'] = csv_info['CPAM0034']
            csv_info.pop('CPAM0034')
    return csv_info

xenopus_tracking_csv = sys.argv[1]

rosalution_auth_header = rosalution_authenticate()

print(f"🧬 Extracting Xenopus Projects from '{xenopus_tracking_csv}'...")
xenopus_projects = read_xenopus_tracking_csv_info(xenopus_tracking_csv)

analyses_to_insert_model = []
for analysis_name in xenopus_projects:
    print_message("🐸", f"Processing {analysis_name}.......")
    xenopus_model_data = xenopus_projects[analysis_name]
    analysis = RosalutionAnalysis(analysis_name, config['ROSALUTION_API_URL'], rosalution_auth_header)

    if not analysis.xenopus_model_system_section_exists():
        analyses_to_insert_model.append(analysis_name)
        continue
    
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

if len(analyses_to_insert_model) > 0:
    print_message("🐸", "Following Rosalution analyses are missing the 'Xenopus Model System' section")
    print(*[f"'{analysis_name}'" for analysis_name in analyses_to_insert_model], sep=" ")