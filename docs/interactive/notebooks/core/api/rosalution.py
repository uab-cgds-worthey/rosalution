import json
import requests
import re
import sys
import urllib3

from ..utils import load_environment, print_message, print_progress, remove_text_in_parentheses

urllib3.disable_warnings()

def rosalution_authenticate():
    """Authenticates and returns the request header to authenticate with Rosalution"""
    config = load_environment()
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
    return {"Authorization": f"Bearer {auth_response_json['access_token']}"}


class Rosalution:
    def __init__(self, rosalution_analysis_name, rosalution_auth_header):
        env_config = load_environment()
        self.analysis_name = rosalution_analysis_name
        self.auth_header = rosalution_auth_header
        self.api_url = env_config["ROSALUTION_API_URL"]

        self.omic_unit_resource_map = {"gene": "gene", "hgvs_variant": "hgvsVariant"}
        self.analysis_cache = {
            'invalid': True,
        }

        self.annotations_cache = {
            'invalid': True,
        }

    @staticmethod
    def projects(auth_header, api_url):
        config = load_environment()
        summary = requests.get(
            f"{api_url}/analysis/summary",
            verify=False,
            timeout=20,
            headers=auth_header,
        )
        summary_json = summary.json()
        return [analysis['name'] for analysis in summary_json] 

    def get_genomic_units(self):
        """
        Retrieve the genomic units from the analysis.
        """
        print(f"{self.api_url}/analysis/{self.analysis_name}/genomic_units")
        response = requests.get(
            f"{self.api_url}/analysis/{self.analysis_name}/genomic_units",
            verify=False,
            timeout=20,
            headers=self.auth_header,
        )

        genomic_units_json = response.json()
        print(json.dumps(genomic_units_json, indent=2))
        genomic_units = {
            "gene": list(genomic_units_json["genes"].keys()),
            "hgvs_variant": list(map(remove_text_in_parentheses, genomic_units_json["variants"])),
        }
        return genomic_units
    
    def get_annotations(self, unit_type: str, unit: str):
        """Fetch annotations for a genomic unit."""
        cache_name = f"{unit_type}_{unit}"

        if cache_name in self.annotations_cache:
            return self.annotations_cache[cache_name]

        response_unit_annotations = requests.get(
            f"{self.api_url}/analysis/{self.analysis_name}/{self.omic_unit_resource_map[unit_type]}/{unit}",
            verify=False,
            timeout=20,
            headers=self.auth_header,
        )

        self.annotations_cache[cache_name] = response_unit_annotations.json()

        if 'invalid' in self.annotations_cache:
            del self.annotations_cache['invalid']

        return self.annotations_cache[cache_name]

    def get_annotation(self, unit_type: str, unit: str, rosalution_annotation_name: str):
        self.get_annotations(unit_type, unit)

        cache_name = f"{unit_type}_{unit}"
        if cache_name not in self.annotations_cache:
            return None
        

        return self.annotations_cache[cache_name].get(rosalution_annotation_name, None)

    def get_analysis(self):
        """ Fetches data about the analysis itself. """

        response_analysis = requests.get(
            f"{self.api_url}/analysis/{self.analysis_name}",
            verify=False,
            timeout=20,
            headers=self.auth_header
        )

        self.analysis_cache = response_analysis.json()

        return self.analysis_cache

    def get_annotation_manifest(self):
        if(not self._is_analysis_cache_set()):
            self.get_analysis()

        return self.analysis_cache['manifest']

    def _is_analysis_cache_set(self):
        return 'invalid' not in self.analysis_cache
    
    def _get_field(self, field: str):
        if(not self._is_analysis_cache_set()):
            self.get_analysis()

        
        value_list = []

        generator = (
                        row['value']
                        for section in self.analysis_cache['sections']
                        for row in section['content']
                        if row['field'] == field
                    )
        for value in generator:
            value_list.append(value)
        
        field_value = next(
            (
                row['value']
                for section in self.analysis_cache['sections']
                for row in section['content']
                if row['field'] == field
            ),
            None,
        )

        return ','.join(field_value) if field_value else None
    
    def get_models_of_interest(self):
        models_of_interest_text = self._get_field('Model of Interest')
        if not models_of_interest_text:
            return []
        return [model.strip() for model in models_of_interest_text.split(',')] 

    def get_existing_collaborators(self):
        collaborators = self._get_field('Existing Collaborations')
        if not collaborators:
            return []
        return collaborators
    
    def get_analysis_descriptive_hpo_terms(self):
        hpo_terms_text = self._get_field('HPO Terms')
        if not hpo_terms_text:
            return []
        return [model.strip() for model in re.split(';|,', hpo_terms_text)] 

    def get_analysis_hpo_terms(self):
        hpo_terms_text = self._get_field('HPO Terms')
        if not hpo_terms_text:
            return []
        return re.findall(r'HP:\d{7}', hpo_terms_text)
