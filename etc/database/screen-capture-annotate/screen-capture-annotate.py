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
import asyncio

import requests

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

config = dotenv_values('.env')

def remove_text_in_parentheses(text):
  return re.sub(r'\([^)]*\)', '', text)

def aggregate_string_replacement(key, value, base_string):
  genomic_unit_string = f"{{{key}}}"
  return base_string.replace(genomic_unit_string, value)

def click_popup(chrome_driver, selector):
  try:
    print(f'{url}: Checking for Popup Element', end='\r', flush=True)
    start_time = time.time()
    popup_element = WebDriverWait(chrome_driver, 10).until(
      lambda driver: driver.find_element(By.CSS_SELECTOR, selector)
    )
    print(f'{url}: Found Popup element {selector}', end='\r', flush=True)
    if popup_element:
        popup_element.click()
  except:
    print(f'{url}: No Popup element', end='\r', flush=True)
  finally:
    end_time = time.time()
    print(f'{url}: {end_time-start_time}: Time elased checking for popup', end='\n', flush=True)

#@ https://local.rosalution.cgds/rosalution/api/analysis/CPAM0002/genomic_units

# - Chromosomal_Locatlization (HGVS_VARIANT)
# - Secondary_Structure (HGVS_VARIANT)
# - Causal_Variant_In_This_Locus_ClinVar (HGVS_VARIANT)
# - Variant_Publications(HGVS_VARIANT)
# GeneHomology_Multi-SequenceAlignmen (HGVS_VARIANT)
# - Human_Gene_Expression - GENE
# - Human_Gene_versus_Protein_Expresssion_Profile GENE
# Model_System_Expression_Profiles
#  - GENE
datasets = {
    "GENE": [
       {
        "dataset": "Druggability", "url": "https://pharos.nih.gov/targets/{GENE}#ppi",
        "dom_attribute": "ppi", "dependencies": [], "selenium_by": By.ID, "popup_selectors": [
         '.shepherd-cancel-icon',
         '.shepherd-cancel-icon',]
    },
      {
        "dataset": "Gene Expression", "url": "https://gtexportal.org/home/gene/{GENE}",
        "dom_attribute": "geneExpression", "dependencies": [], "selenium_by": By.ID,
    },
      {
      "dataset": "Orthology", "url": "https://www.alliancegenome.org/gene/{HGNC_ID}",
      "dom_attribute": "a#orthology", "dependencies": ["HGNC_ID"], "selenium_by": By.CSS_SELECTOR,
    },
      {
      "dataset": "Human_Gene_vs_Protein_Expression_Profile", "url": "https://www.proteinatlas.org/{Ensembl Gene Id}-{GENE}/tissue",
      "dom_attribute": "//table[@class='main_table']/tbody/tr/td[2]/div[@class='tissue_summary menu_margin']/table[@class='darkheader_white'][1]/tbody/tr[@class='roundbottom']", "dependencies": ["Ensembl Gene Id"], "selenium_by": By.XPATH,
    }
    ],
    "VARIANT": [{

    }],
}

response = requests.get(f"{config['ROSALUTION_API_URL']}analysis/CPAM0002/genomic_units", verify=False)
genomic_units_json = response.json()
genomic_units = {
  "GENES": list(genomic_units_json['genes'].keys()),
  "VARIANT": list(map(remove_text_in_parentheses, genomic_units_json['variants']))
}

# Configure Chrome WebDriver options
options = Options()
options.add_argument("--window-size=1920,1080")
options.add_argument("--start-maximized")
# options.add_argument("--headless")
options.add_argument("--disable-gpu")

# Initialize the Chrome WebDriver
driver = webdriver.Chrome(options=options)
driver.maximize_window()

path = os.path.dirname(os.path.abspath(__file__))

for gene_dataset in datasets["GENE"]:
    for gene in genomic_units["GENES"]:
      url = aggregate_string_replacement('GENE', gene, gene_dataset['url'])

      response_gene_annotations = requests.get(f"{config['ROSALUTION_API_URL']}annotation/gene/{gene}", verify=False)
      gene_annotations = response_gene_annotations.json()
      for dependency in gene_dataset['dependencies']:
        if dependency in gene_annotations:
          url = aggregate_string_replacement(dependency, gene_annotations[dependency], url)
      
      print(url, end='\r', flush=True)

      # Get the current timestamp for the image name
      today = datetime.now()
      image_name = today.strftime("%Y-%m-%d %H:%M:%S")
      image_name = f"{gene}-{gene_dataset['dataset']}-{image_name}"

      # Set the path where the screenshot will be saved

      print(f'{url}: Visiting', end='\r', flush=True)

      driver.get(url)

      # print(driver.page_source)
      # print(driver.find('pip'))

      width = driver.execute_script(
          "return Math.max( document.body.scrollWidth, document.body.offsetWidth, document.documentElement.clientWidth, document.documentElement.scrollWidth, document.documentElement.offsetWidth );"
      )
      height = driver.execute_script(
          "return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );"
      )

      driver.set_window_size(width, height)

      if 'popup_selectors' in gene_dataset:
        for selector in gene_dataset['popup_selectors']:
          click_popup(driver, selector) 

      try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((gene_dataset['selenium_by'], gene_dataset["dom_attribute"]))
        )
      except TimeoutException as err:
          raise TimeoutError("Page not loaded") from err

      page_element = driver.find_element(gene_dataset['selenium_by'], gene_dataset["dom_attribute"])
      print(f'{url}: Found visualization, saving image', end='\r', flush=True)
      page_element.screenshot(f"tmp/{image_name}.png")
      print(f'{url}: Saving Operation Complete              ', end='\n', flush=True)


# Close the browser window
driver.quit()

# Get genomic units from the analysis
