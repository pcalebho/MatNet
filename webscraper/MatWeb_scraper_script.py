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
from tabulate import tabulate

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
        with click.progressbar(range(1), label= bar_label) as bar:
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
    soup = BeautifulSoup(driver.page_source,'html.parser')

    #Third table in html page has correct content
    table = soup.find_all("table", class_ = "tabledataformat")
    table = table[2]

    
    table_body = table.find('tbody')
    table_list = []
    table_list_ix: int = 0
    rows = table_body.find_all('tr')
    data = []
    
    #This creates a list of tables from the main content table. 
    for row in rows:
        cols = row.find_all(['td'])

        #necessary to delimit tables within content tables
        if not cols:
            data = []
            cols = row.find_all(['th'])
            table_list.append(data)
            table_list_ix += 1

        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele]) # Get rid of empty values
    
    table_list.append(data)
    
    #Used for removing all the empty rows in each individual table
    for i in range(len(table_list)):
        table_list[i] = [x for x in table_list[i] if x != []]


    #have type checker ignore None type error
    material_name = soup.find('title').get_text() # pyright: ignore[reportOptionalMemberAccess]
    material_name = material_name.strip()

    print(material_name)
    # print(data)
    for t in table_list:
        print(tabulate(t))
    
    print(table_list[0])

    


if __name__ == '__main__':
    test1 = '/search/DataSheet.aspx?MatGUID=7b75475aa1bc41618788f63c6500d36b'
    test2 = '/search/DataSheet.aspx?MatGUID=210fcd12132049d0a3e0cabe7d091eef'
    options = Options()
    options.add_experimental_option("detach",True)
    options.add_argument('--headless')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), \
                              options=options)

    # results = search_material_pages(searches=['AISI'],driver= driver)
    # print('Number of results: ', len(results))
    # print(results)
    parse_table(test1,driver)
    # print(dataframe[0].head())

    driver.quit()
    print('Done')

# print(next_page_link)
# print(soup.prettify())