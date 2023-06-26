from bs4 import BeautifulSoup
import pandas as pd
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import click

def search_material_pages(searches: list[str]) -> list[str]:
    material_pages = []
    url_list = []

    options = Options()
    options.add_experimental_option("detach",True)
    options.add_argument('--headless')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)

    [url_list.append('https://matweb.com/search/QuickText.aspx?SearchText=' + search) for search in searches]

    i = 1

    for url in url_list:
        driver.get(url)

        #Number of pages are used for the end condition of the loop
        page_select_button = driver.find_element(By.NAME, 'ctl00$ContentMain$ucSearchResults1$drpPageSelect1')
        pages = page_select_button.find_elements(By.TAG_NAME, 'option')


        next_button = driver.find_element(By.ID, 'ctl00_ContentMain_ucSearchResults1_lnkNextPage')

        bar_label = "'%s' +  (%i/%i)" % (searches[i], i , len(searches))
        with click.progressbar(pages, label= bar_label) as bar:
            for page in bar:
                next_button = driver.find_element(By.ID, 'ctl00_ContentMain_ucSearchResults1_lnkNextPage')
                
                next_button.click()
                time.sleep(1)

                soup = BeautifulSoup(driver.page_source, 'html.parser')

                #Find and store all the material links on the page 
                for link in soup.find_all('a', id = re.compile('^lnkMatl')):
                    material_pages.append(link.get('href')) 
         
        i += 1

    driver.quit()
    return(material_pages)


if __name__ == '__main__':
    result = search_material_pages(['AISI','aluminum'])
    print('Number of results: ', len(result))

# print(next_page_link)
# print(soup.prettify())