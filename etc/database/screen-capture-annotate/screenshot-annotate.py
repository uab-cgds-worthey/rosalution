from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os
from datetime import datetime
from dotenv import dotenv_values

import requests

config = dotenv_values('.env')



#@ https://local.rosalution.cgds/rosalution/api/analysis/CPAM0002/genomic_units

# Get the current timestamp for the image name
today = datetime.now()
image_name = today.strftime("%Y-%m-%d %H:%M:%S")

# Set the path where the screenshot will be saved
path = os.path.dirname(os.path.abspath(__file__))

# Configure Chrome WebDriver options
options = Options()
options.add_argument("--window-size=1920,1080")
options.add_argument("--start-maximized")
options.add_argument("--headless")
options.add_argument("--disable-gpu")

# Initialize the Chrome WebDriver
driver = webdriver.Chrome(options=options)
driver.maximize_window()




driver.get("https://gtexportal.org/home/gene/CEP104")

time.sleep(1)

width = driver.execute_script("return Math.max( document.body.scrollWidth, document.body.offsetWidth, document.documentElement.clientWidth, document.documentElement.scrollWidth, document.documentElement.offsetWidth );")
height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")

driver.set_window_size(width, height)

full_page = driver.find_element(By.ID, "gene-expr-vplot")
full_page.screenshot(f"{image_name}.png")

# Close the browser window
driver.quit()



# Get genomic units from the analysis