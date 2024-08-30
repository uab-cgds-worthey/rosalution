"""
Script: genomic_unit_screenshot.py

Description:
This script automates the process of capturing screenshots of web-based genomic data visualizations. 
Using Selenium, it navigates to specified urls for different genomic datasets, and saves the screenshot 
to a /tmp directory within the current directory.

Usage:
1. Ensure the `.env` file contains the required
    a. `ROSALUTION_CLIENT_ID` & `ROSALUTION_CLIENT_SECRET` for your Rosalution user
    b. `ROSALUTION_API_URL` for the target Rosalution, ex. https://local.rosalution.cgds/rosalution/api/
2. Provide list of Rosalution analyses to create screen captures for. Important to note, that if there are spaces
   within the name of an analysis, it must be surounded by double or single quotes.

Output:
- Screenshots saved in the `tmp/` directory with filenames that follow the pattern:
    `{genomic_unit}-{dataset}-{date}.png`
"""
import contextlib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os
from datetime import datetime
from dotenv import dotenv_values
import re
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

import requests

import urllib3
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

config = dotenv_values('.env')


DATASETS = {
    "gene": [{
        "dataset": "Druggability", "url": "https://pharos.nih.gov/targets/{gene}#ppi", "dom_attribute": "ppi",
        "extra_dom_element_wait": "circle",
        "dependencies": [], "selenium_by": By.ID, "popup_selectors": [
            '.shepherd-cancel-icon',
            '.shepherd-cancel-icon',
        ]
    }, {
        "dataset": "Gene Expression",
        "url": "https://gtexportal.org/home/gene/{gene}",
        "dom_attribute": "geneExpression",
        "dependencies": [],
        "selenium_by": By.ID,
    }, {
        "dataset": "Orthology",
        "url": "https://www.alliancegenome.org/gene/{HGNC_ID}",
        "dom_attribute": "a#orthology",
        "dependencies": ["HGNC_ID"],
        "selenium_by": By.CSS_SELECTOR,
    }, {
        "dataset": "Human_Gene_vs_Protein_Expression_Profile",
        "url": "https://www.proteinatlas.org/{Ensembl Gene Id}-{gene}/tissue",
        "dom_attribute":
            "//table[@class='main_table']/tbody/tr/td[2]/div[@class='tissue_summary menu_margin']/table[@class='darkheader_white'][1]/tbody/tr[@class='roundbottom']",
        "dependencies": ["Ensembl Gene Id"],
        "selenium_by": By.XPATH,
    }],
    "hgvsVariant": [],
}


def remove_text_in_parentheses(text):
    return re.sub(r'\([^)]*\)', '', text)


def aggregate_string_replacement(key, value, base_string):
    genomic_unit_string = f"{{{key}}}"
    return base_string.replace(genomic_unit_string, value)

class ScreenCaptureDatasets(contextlib.ExitStack):
    def __init__(self):
        super().__init__()
        self.captured_datasets = {}
    
    def __enter__(self):
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

    def __exit__(self, *exec):
        self.driver.__exit__(*exec)
    
    def click_popup(self, url, selector):
        try:
            print(f'{url}: Checking for Popup Element', end='\r', flush=True)
            start_time = time.time()
            popup_element = WebDriverWait(self.driver,
                                        10).until(lambda driver: driver.find_element(By.CSS_SELECTOR, selector))
            print(f'{url}: Found Popup element {selector}', end='\r', flush=True)
            if popup_element:
                popup_element.click()
        except:
            print(f'{url}: No Popup element', end='\r', flush=True)
        finally:
            end_time = time.time()
            print(f'{url}: {end_time-start_time}: Time elased checking for popup', end='\n', flush=True)

    def screencapture_dataset(self, unit_type, unit, unit_annotations, dataset):
        url = aggregate_string_replacement(unit_type, unit, dataset['url'])

        for dependency in dataset['dependencies']:
            if dependency in unit_annotations:
                url = aggregate_string_replacement(dependency, unit_annotations[dependency], url)

        print(url, end='\r', flush=True)

        # Get the current timestamp for the image name
        today = datetime.now()
        image_name = today.strftime("%Y-%m-%d")
        image_name = f"{unit}-{dataset['dataset']}-{image_name}"

        # Set the path where the screenshot will be saved
        print(f'{url}: Visiting', end='\r', flush=True)

        self.driver.get(url)

        width = self.driver.execute_script(
            "return Math.max( document.body.scrollWidth, document.body.offsetWidth, document.documentElement.clientWidth, document.documentElement.scrollWidth, document.documentElement.offsetWidth );"
        )
        height = self.driver.execute_script(
            "return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );"
        )

        self.driver.set_window_size(width, height)

        if 'popup_selectors' in dataset:
            for selector in dataset['popup_selectors']:
                self.click_popup(url, selector)

        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((dataset['selenium_by'], dataset["dom_attribute"]))
            )

            if "extra_dom_element_wait" in dataset:
                WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.TAG_NAME,"circle"))
                )
        except TimeoutException as err:
            print(f'{url}: Failed to locate visualization {err}', end='\r', flush=True)
            return None

        page_element = self.driver.find_element(dataset['selenium_by'], dataset["dom_attribute"])
        print(f'{url}: Found visualization, saving image', end='\r', flush=True)
        file_name = f"tmp/{image_name}.png"
        page_element.screenshot(file_name)

        print(f'{url}: Saving Operation Complete              ', end='\n', flush=True)
        return file_name


class RosalutionAnalysis():
    def __init__(self, analysis_name):
        self.analysis_name = analysis_name

    def get_genomic_units(self):
        response = requests.get(f"{config['ROSALUTION_API_URL']}analysis/{self.analysis_name}/genomic_units", verify=False)
        genomic_units_json = response.json()
        genomic_units = {
            "gene": list(genomic_units_json['genes'].keys()),
            "hgvsVariant": list(map(remove_text_in_parentheses, genomic_units_json['variants']))
        }
        return genomic_units
    
    def get_annotations(self, type, unit):
        response_unit_annotations = requests.get(f"{config['ROSALUTION_API_URL']}annotation/{type}/{unit}", verify=False)
        return response_unit_annotations.json()
    
    def capture_analysis(self, capture):
        genomic_units = self.get_genomic_units()
        for genomic_unit_type in genomic_units.keys():
            for unit in genomic_units[genomic_unit_type]:
                unit_annotations = self.get_annotations(genomic_unit_type, unit)
                for genomic_unit_dataset in DATASETS[genomic_unit_type]:
                    capture.screencapture_dataset(genomic_unit_type, unit, unit_annotations, genomic_unit_dataset)

rosalution_analyses = sys.argv[1:]

print("Capturing Rosalution Analyses")
print(*[ f"   🧬 {analysis}" for analysis in rosalution_analyses], sep="\n")

with ScreenCaptureDatasets() as capture:
    for analysis_name in rosalution_analyses:
        analysis = RosalutionAnalysis(analysis_name)
        analysis.capture_analysis(capture)

