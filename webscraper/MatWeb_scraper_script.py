from bs4 import BeautifulSoup
import pandas as pd
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import ByS
import click
from tabulate import tabulate
import yaml

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
    '''Is used for parsing a content table from MatWeb'''
    material_page = 'https://matweb.com' + material_path
    driver.get(material_page)
    soup = BeautifulSoup(driver.page_source,'html.parser')
    table = soup.find_all("table", class_ = "tabledataformat")

    #find supplementary notes in tables
    matl_notes_table = table[1].find(id= "ctl00_ContentMain_ucDataSheet1_trMatlNotes")
    category_table = table[1].find(id= "ctl00_ContentMain_ucDataSheet1_trMatlGroups")
    
    categories = category_table.find('td').text 
    material_notes = matl_notes_table.find('td').text  
        

    #Third table in html page has correct content
    main_table = table[2].find('tbody')
    property_tables = []
    property_tables_ix: int = 0
    rows = main_table.find_all('tr')
    data = []
    
    #This creates a list of tables from the main content table. 
    for row in rows:
        cols = row.find_all('td')

        #necessary to delimit tables within content tables
        if not cols:
            data = []
            cols = row.find_all('th')
            property_tables.append(data)
            property_tables_ix += 1

        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele]) # Get rid of empty values
    
    property_tables.append(data)
    
    #Used for removing all the empty rows in each individual table
    for i in range(len(property_tables)):
        property_tables[i] = [x for x in property_tables[i] if x != []]

    #find name of material in page and remove unnecessary whitespace
    material_name = soup.find('title').get_text() # pyright: ignore[reportOptionalMemberAccess]
    material_name = material_name.strip()

    return (material_name, {'notes': material_notes, 'category': categories, 'properties': property_tables})

def write_yaml_file(file_path, data):
    with open(file_path, 'a') as file:
        yaml.dump(data, file)
    

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
    (material_name, data) = parse_table(test1,driver)
    print(material_name)
    print(data['notes'])
    print(data['category'])
    property_tables = data['properties']
    for t in property_tables:
        print(tabulate(t))

    driver.quit()
    print('Done')

# print(next_page_link)
# print(soup.prettify())