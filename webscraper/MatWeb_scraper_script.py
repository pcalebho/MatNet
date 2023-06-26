from bs4 import BeautifulSoup
import pandas as pd
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import requests
import click

def search_material_pages(searches: list[str], driver) -> list[str]:
    material_pages = []
    url_list = []

    [url_list.append('https://matweb.com/search/QuickText.aspx?SearchText=' + search) for search in searches]

    i = 0
    for url in url_list:
        #Open chrome window
        driver.get(url)

        #Number of pages are used for the end condition of the loop
        page_select_button = driver.find_element(By.NAME, 'ctl00$ContentMain$ucSearchResults1$drpPageSelect1')
        pages = page_select_button.find_elements(By.TAG_NAME, 'option')

        #Used for pagination
        next_button = driver.find_element(By.ID, 'ctl00_ContentMain_ucSearchResults1_lnkNextPage')

        bar_label = "'%s' (%i/%i)" % (searches[i], i+1 , len(searches))
        with click.progressbar(pages, label= bar_label) as bar:
            for page in bar:
                time.sleep(1)

                soup = BeautifulSoup(driver.page_source, 'html.parser')

                #Find and store all the material links on the page 
                for link in soup.find_all('a', id = re.compile('^lnkMatl')):
                    material_pages.append(link.get('href')) 

                next_button = driver.find_element(By.ID, 'ctl00_ContentMain_ucSearchResults1_lnkNextPage')
                next_button.click()
         
        i += 1

    return(material_pages)

def parse_table(material_path: str, driver):
    material_page = 'https://matweb.com' + material_path
    driver.get(material_page)
    df = pd.read_html(material_page)
    return df
    # soup = BeautifulSoup(driver.page_source, 'html.parser')



if __name__ == '__main__':
    options = Options()
    options.add_experimental_option("detach",True)
    options.add_argument('--headless')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), \
                              options=options)

    results = search_material_pages(searches=['AISI'],driver= driver)
    print('Number of results: ', len(results))

    print(results)
    # dataframe = parse_table(results[0],driver)
    # print(dataframe[0].head())

    driver.quit()
    print('Done')

# print(next_page_link)
# print(soup.prettify())