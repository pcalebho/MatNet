from bs4 import BeautifulSoup
import pandas as pd
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

material_pages = []

options = Options()
options.add_experimental_option("detach",True)
options.add_argument('--headless')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
searches = ['AISI', 'aluminum']

url = 'https://matweb.com/search/QuickText.aspx?SearchText=' + searches[0]

driver.get(url)

#Number of pages are used for the end condition of the loop
page_select_button = driver.find_element(By.NAME, 'ctl00$ContentMain$ucSearchResults1$drpPageSelect1')
pages = page_select_button.find_elements(By.TAG_NAME, 'option')


next_button = driver.find_element(By.ID, 'ctl00_ContentMain_ucSearchResults1_lnkNextPage')

for page in pages:
    next_button = driver.find_element(By.ID, 'ctl00_ContentMain_ucSearchResults1_lnkNextPage')
    
    next_button.click()
    time.sleep(1)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    #Find and store all the material links on the page 
    for link in soup.find_all('a', id = re.compile('^lnkMatl')):
        material_pages.append(link.get('href')) 


print(material_pages)
print('Number of Results: ', len(material_pages))
driver.quit()



# print(next_page_link)
# print(soup.prettify())