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
import os
import re
import sys
import time
from datetime import datetime
import urllib3

from dotenv import dotenv_values

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

import requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

config = dotenv_values('.env')

FORCE_APPEND = 'FORCE_APPEND' in config and (config['FORCE_APPEND'].lower() in ('true', '1', 't', 'on'))

OVERWRITE_LOCAL_SAVE = 'OVERWRITE_LOCAL_SAVE' in config and (
    config['OVERWRITE_LOCAL_SAVE'].lower() in ('true', '1', 't', 'on')
)

DATASETS = {
    "gene": [
        {
            "dataset": "Druggability", "url": "https://pharos.nih.gov/targets/{gene}",
            "dom_attribute": "scrollspy-main", "extra_dom_element_wait": "pharos-radar-chart", "dependencies": [],
            "selenium_by": By.ID, "popup_selectors": [
                '.shepherd-cancel-icon',
                '.shepherd-cancel-icon',
            ], "additional_script_execution":
                """
            document.querySelectorAll('mat-card').forEach(el => {
                if (el.id !== 'development' && el.id !== 'ppi' && !el.classList.contains('target-card')) {
                    el.remove();
                }
            });
        """
        },
        {
            "dataset": "Human_Gene_Expression",
            "url": "https://gtexportal.org/home/gene/{gene}",
            "dom_attribute": "geneExpression",
            "extra_dom_element_wait": "svg",
            "file_postfix": "-0",
            "dependencies": [],
            "selenium_by": By.ID,
        },
        {
            "dataset": "Human_Gene_Expression",
            "url": "https://www.proteinatlas.org/{Ensembl Gene Id}-{gene}/single+cell+type",
            "dependencies": ["Ensembl Gene Id"],
            "selenium_by": By.XPATH,
            "file_postfix": "-1",
            "dom_attribute": "(//table[contains(@class, \"main_table\")])",  #pylint: disable=line-too-long
            "additional_script_execution":
                """
            let tables = document.evaluate(
                '(//table[contains(@class, "main_table")])[1]//table',
                document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null
            );
            for (let i = 3; i < tables.snapshotLength; i++) tables.snapshotItem(i).remove();
            """
        },
        {
            "dataset": "Orthology",
            "url": "https://www.alliancegenome.org/gene/{HGNC_ID}",
            "dom_attribute": "a#orthology",
            "dependencies": ["HGNC_ID"],
            "selenium_by": By.CSS_SELECTOR,
        },
        {
            "dataset": "Human_Gene_versus_Protein_Expression_Profile",
            "url": "https://www.proteinatlas.org/{Ensembl Gene Id}-{gene}/tissue",
            "dom_attribute":
                "//table[@class='main_table']/tbody/tr/td[2]/div[@class='tissue_summary menu_margin']/table[@class='darkheader_white'][1]/tbody/tr[@class='roundbottom']",  #pylint: disable=line-too-long
            "dependencies": ["Ensembl Gene Id"],
            "selenium_by": By.XPATH,
        }
    ],
    "hgvsVariant": [
        # Disabling this annotaiton until additional time can be investigated to support
        # more then just SNV variants for this.
        #     {
        #     "dataset": "GeneHomology_Multi-SequenceAlignment",
        #     "url": "https://marrvel.org/human/variant/{hgvsVariant}",
        #     "dom_attribute":
        #         "app-diopt-alignment", #pylint: disable=line-too-long
        #     "selenium_by": By.TAG_NAME ,
        #     "dependencies": [],
        # }
    ],
}


def remove_text_in_parentheses(text):
    """Remove any text within parentheses from the text string."""
    return re.sub(r'\([^)]*\)', '', text)


def aggregate_string_replacement(key, value, base_string):
    """Replace placeholders in the base string with corresponding values."""
    genomic_unit_string = f"{{{key}}}"
    return base_string.replace(genomic_unit_string, value)


class ScreenCaptureDatasets(contextlib.ExitStack):
    """Manages Selenium WebDriver to capture screenshots of genomic datasets."""

    def __init__(self):
        """Initializes the WebDriver and filepath"""
        super().__init__()
        self.driver = None
        self.path = None

    def __enter__(self):
        """Start the WebDriver session with appropriate configurations."""
        super().__enter__()

        # Configure Chrome WebDriver options
        options = Options()
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--start-maximized")
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")

        # Initialize the Chrome WebDriver
        self.driver = webdriver.Chrome(options=options).__enter__()
        self.driver.maximize_window()

        self.path = os.path.dirname(os.path.abspath(__file__))
        return self

    def __exit__(self, *exec):  # pylint: disable=redefined-builtin
        """Clean up WebDriver resources on exit."""
        super().__exit__(*exec)
        self.driver.__exit__(*exec)

    def click_popup(self, url, selector):
        """Handles pop-up interactions by clicking specified pop-up selector."""
        start_time = time.time()
        try:
            print(f'{url}: Checking for Popup Element', end='\r', flush=True)
            popup_element = WebDriverWait(self.driver,
                                          22).until(lambda driver: driver.find_element(By.CSS_SELECTOR, selector))
            print(f'{url}: Found Popup element {selector}', end='\r', flush=True)
            if popup_element:
                popup_element.click()
        except TimeoutException:
            print(f'{url}: No Popup element', end='\r', flush=True)
        finally:
            end_time = time.time()
            print(f'{url}: {end_time-start_time}: Time elased checking for popup', end='\n', flush=True)

    def screencapture_dataset(self, unit_type, unit, unit_annotations, dataset):
        """Screen capture of a specified genomic unit for a dataset."""
        url = aggregate_string_replacement(unit_type, unit, dataset['url'])

        for dependency in dataset['dependencies']:
            if dependency in unit_annotations:
                url = aggregate_string_replacement(dependency, unit_annotations[dependency], url)

        print(url, end='\r', flush=True)

        # Get the current timestamp for the image name
        postfix = '' if 'file_postfix' not in dataset else dataset['file_postfix']
        image_name = datetime.now().strftime("%Y-%m-%d")
        image_name = f"{unit}-{dataset['dataset']}-{image_name}{postfix}"
        file_name = f"tmp/{image_name}.png"

        if os.path.exists(file_name) and (not OVERWRITE_LOCAL_SAVE):
            print(f'{url}: Skipping Save Operation, File Exists           ', end='\n', flush=True)
            return file_name

        # Set the path where the screenshot will be saved
        print(f'{url}: Visiting', end='\r', flush=True)

        self.driver.get(url)

        width = self.driver.execute_script(
            "return Math.max( document.body.scrollWidth, document.body.offsetWidth, document.documentElement.clientWidth, document.documentElement.scrollWidth, document.documentElement.offsetWidth );"  # pylint: disable=line-too-long
        )
        height = self.driver.execute_script(
            "return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );"  # pylint: disable=line-too-long
        )

        self.driver.set_window_size(width, height)

        if 'popup_selectors' in dataset:
            for selector in dataset['popup_selectors']:
                self.click_popup(url, selector)

        try:
            WebDriverWait(self.driver, 200).until(
                EC.presence_of_element_located((dataset['selenium_by'], dataset["dom_attribute"]))
            )

            if "extra_dom_element_wait" in dataset:
                WebDriverWait(self.driver, 60).until(
                    EC.presence_of_element_located((By.TAG_NAME, dataset['extra_dom_element_wait']))
                )
                time.sleep(20)
        except TimeoutException as err:
            print(f'{url}: Failed to locate visualization {err}', end='\r', flush=True)
            return None

        page_element = self.driver.find_element(dataset['selenium_by'], dataset["dom_attribute"])
        print(f'{url}: Found visualization, saving image', end='\r', flush=True)

        if 'additional_script_execution' in dataset:
            self.driver.execute_script(dataset['additional_script_execution'])

        page_element.screenshot(file_name)

        print(f'{url}: Saving Operation Complete              ', end='\n', flush=True)
        return file_name


class RosalutionAnalysis():
    """
    Representing a Rosalution analysisf for genomic units and annotations,
    and screencaptures datasets to save.
    """

    def __init__(self, analysis_name_string, rosalution_auth_header):
        """Initialize the Rosalution screencapture analyses"""
        self.analysis_name = analysis_name_string
        self.captured_datasets = {}
        self.auth_header = rosalution_auth_header

    def get_genomic_units(self):
        """
        Retrieve the genomic units from the analysis.
        """
        response = requests.get(
            f"{config['ROSALUTION_API_URL']}analysis/{self.analysis_name}/genomic_units", verify=False, timeout=20
        )

        genomic_units_json = response.json()
        genomic_units = {
            "gene": list(genomic_units_json['genes'].keys()),
            "hgvsVariant": list(map(remove_text_in_parentheses, genomic_units_json['variants']))
        }
        return genomic_units

    def get_annotations(self, unit_type, unit):
        """Fetch annotations for a genomic unit."""
        response_unit_annotations = requests.get(
            f"{config['ROSALUTION_API_URL']}analysis/{self.analysis_name}/{unit_type}/{unit}", verify=False, timeout=20
        )
        return response_unit_annotations.json()

    def capture_analysis(self, screen_capture):
        """Capture datasets associated with genomic units in th analysis."""
        genomic_units = self.get_genomic_units()
        for genomic_unit_type, genomic_unit in genomic_units.items():
            for unit in genomic_unit:
                unit_annotations = self.get_annotations(genomic_unit_type, unit)
                if unit == "EXOC3L2":
                    unit_annotations["Ensembl Gene Id"] = "ENSG00000283632"
                if unit == "FOPNL":
                    unit_annotations["HGNC_ID"] = "HGNC:26435"
                    unit_annotations["Ensembl Gene Id"] = "ENSG00000133393"
                for genomic_unit_dataset in DATASETS[genomic_unit_type]:
                    captured_dataset_filepath = screen_capture.screencapture_dataset(
                        genomic_unit_type, unit, unit_annotations, genomic_unit_dataset
                    )
                    if captured_dataset_filepath:
                        extra_in_set = (genomic_unit_dataset['file_postfix']
                                       ) if 'file_postfix' in genomic_unit_dataset else ()
                        self.captured_datasets[
                            (genomic_unit_type, unit, genomic_unit_dataset['dataset'],
                             *extra_in_set)] = captured_dataset_filepath

    def save_to_rosalution(self):
        """Save captured dataset screenshots to the Rosalution API."""
        types_and_genes = {(key[0], key[1]) for key in self.captured_datasets}
        annotations = {}
        for each_unit in types_and_genes:
            unit_type, unit = each_unit
            annotations[(unit_type, unit)] = self.get_annotations(unit_type, unit)

        for entry, file_path in self.captured_datasets.items():
            unit_type, unit, dataset, *post = entry  #pylint: disable=unused-variable
            not_empty = dataset in annotations[(unit_type, unit)] and len(annotations[(unit_type, unit)][dataset]) > 0
            if not_empty and (not FORCE_APPEND):
                print(f'{entry}: Upload Operation Skipped, Annotation Exists          ', end='\n', flush=True)
                continue
            self.upload_file_to_rosalution(entry, file_path)

    def upload_file_to_rosalution(self, entry: tuple, file_path: str):
        """Uploads spceific file to the dataset entry"""
        unit_type, unit, dataset, *post = entry  #pylint: disable=unused-variable
        api_url = \
            f"{config['ROSALUTION_API_URL']}annotation/{unit}/{dataset}/attachment?genomic_unit_type={unit_type}"
        filename = file_path.strip('/')[1]

        with open(file_path, 'rb') as captured_dataset:
            files = {'upload_file': (filename, captured_dataset, 'application/png', {'Expires': '0'})}

            print(f'{entry}: Upload Operation Begin              ', end='\r', flush=True)
            response = requests.post(api_url, headers=self.auth_header, files=files, verify=False, timeout=20)
            result_text = "Success" if response.status_code in [200, 201] else "Failed"
            print(f'{entry}: Upload Operation {result_text}              ', end='\n', flush=True)


def rosalution_authenticate():
    """ Authenticates and returns the request header to authenticate with Rosalution """
    print('🔒 Authenticating with Rosalution...', end='\r', flush=True)
    client_id, client_secret = config['ROSALUTION_CLIENT_ID'], config['ROSALUTION_CLIENT_SECRET']
    auth_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    auth_data = \
        f"grant_type=&scope=&client_id={client_id}&client_secret={client_secret}"
    auth_response = requests.post(
        f"{config['ROSALUTION_API_URL']}auth/token", headers=auth_headers, data=auth_data, verify=False, timeout=20
    )
    auth_response_json = auth_response.json()
    if 'access_token' not in auth_response_json:
        print('🔒 Authenticating with Rosalution...Failed', end='\n', flush=True)
        print(auth_response_json)
        sys.exit(2)

    print('🔓 Authenticating with Rosalution...Complete', end='\n', flush=True)
    return {'Authorization': f"Bearer {auth_response_json['access_token']}"}


rosalution_analyses = sys.argv[1:]

rosalution_header = rosalution_authenticate()

print("📷 Capturing Rosalution Analyses")
print(*[f"   🧬 {analysis}" for analysis in rosalution_analyses], sep="\n")

with ScreenCaptureDatasets() as capture:
    for analysis_name in rosalution_analyses:
        analysis = RosalutionAnalysis(analysis_name, rosalution_header)
        analysis.capture_analysis(capture)
        analysis.save_to_rosalution()
