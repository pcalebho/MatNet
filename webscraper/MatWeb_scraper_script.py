from bs4 import BeautifulSoup
import re
import time
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import click
from tabulate import tabulate
import yaml
import random
import os
from list_manipulation import group_lists
import urllib.request
import requests

#OXYLABS PROXY INFO
USERNAME = "pcho69"
PASSWORD = "StealthyWebsitePumpk1n"
ENDPOINT = "pr.oxylabs.io:7777"

def search_by_keyword(searches: list[str], driver, debug=False) -> list[str]:
    '''
        Returns a list of strings 
        Parameters: 
    '''
    material_pages = []
    url_list = []

    [url_list.append(
        'https://matweb.com/search/QuickText.aspx?SearchText=' + search)\
              for search in searches]

    i = 0
    for url in url_list:
        #Open chrome window
        driver.get(url)

        #Number of pages are used for the end condition of the loop
        page_select_button = driver.find_element(
            By.NAME, 'ctl00$ContentMain$ucSearchResults1$drpPageSelect1')
        pages = page_select_button.find_elements(By.TAG_NAME, 'option')

        #Used for pagination
        next_button = driver.find_element(
            By.ID, 'ctl00_ContentMain_ucSearchResults1_lnkNextPage')

        bar_label = "'%s' (%i/%i)" % (searches[i], i+1 , len(searches))
        
        #Will only search one page if debug is true
        num_pages = len(pages)
        if debug:
            num_pages = 1

        with click.progressbar(range(num_pages), label= bar_label) as bar:
            for page in bar:
                try:
                    WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((
                            By.ID, 'ctl00_ContentMain_ucSearchResults1_lnkNextPage'))
                    )
                except Exception:
                    raise Exception('Timeout')

                soup = BeautifulSoup(driver.page_source, 'html.parser')

                #Find and store all the material links on the page 
                for link in soup.find_all('a', id = re.compile('^lnkMatl')):
                    material_pages.append(link.get('href')) 

                next_button = driver.find_element(
                    By.ID, 'ctl00_ContentMain_ucSearchResults1_lnkNextPage')
                next_button.click()
         
        i += 1

    return(material_pages)

def search_by_property():
    pass

def scrape(material_paths) -> list[dict]:
    result: list[dict] = []
    entry = ('http://customer-%s:%s@pr.oxylabs.io:7777' %
        (USERNAME, PASSWORD))
    query = {
        'http': entry,
        'https': entry,
    }

    for relative_path in material_paths:
        proxies = query
        path = 'https://matweb.com' + relative_path

        response = requests.get(
            url=path,
            proxies= proxies,
            verify=True
        )
        soup = BeautifulSoup(response.content,'lxml')
        result.append(parse_table(soup))    
    
    return result


def parse_table(soup):
    '''Is used for parsing a content table from MatWeb'''
    table = soup.find_all("table", class_ = "tabledataformat")
    if len(table) != 3:
        raise Exception('IP Blocked')

    #find supplementary notes in tables
    matl_notes_table = table[1].find(id= "ctl00_ContentMain_ucDataSheet1_trMatlNotes")
    category_table = table[1].find(id= "ctl00_ContentMain_ucDataSheet1_trMatlGroups")
    
    material_notes = None
    categories = None

    try:
        if matl_notes_table is not None:
            material_notes = matl_notes_table.find('td').text
        
        if category_table is not None:
            categories = category_table.find('td').text 
    except Exception:
        exception_msg = 'Issues with grabbing material and category notes: ' \
            + pages
        print(exception_msg)
        

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
    material_name = soup.find('title').get_text() # pyright: ignore[reportOptionalMemberAccess]  # noqa: E501
    material_name = material_name.strip()

    return {'name': material_name,'notes': material_notes, \
            'category': categories, 'properties': property_tables}


def write_yaml_file(file_path, data, overwrite= False):
    if not overwrite:
        with open(file_path, 'a') as file:
            yaml.dump(data, file)
    else:
        with open(file_path, 'w') as file:
            yaml.dump(data, file)
            

def selenium_proxy(user: str, password: str, endpoint: str) -> dict:
    wire_options = {
        "proxy": {
            "http": f"http://{user}:{password}@{endpoint}",
            "https": f"http://{user}:{password}@{endpoint}",
        }
    }

    return wire_options

def write_to_log(log_file: str, error_msg: str):
    with open(log_file, 'a') as file:
        file.write(error_msg)
        

if __name__ == '__main__':
    start = time.time()
    test1 = '/search/DataSheet.aspx?MatGUID=7b75475aa1bc41618788f63c6500d36b'
    test2 = '/search/DataSheet.aspx?MatGUID=210fcd12132049d0a3e0cabe7d091eef'
    options = Options()
    options.add_experimental_option("detach",True)
    options.add_argument('--headless')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')

    proxies = selenium_proxy(USERNAME,PASSWORD,ENDPOINT)
    #service=Service(ChromeDriverManager().install()), \
    driver = webdriver.Chrome(options=options, seleniumwire_options=proxies)
    
    matdata_list =[]
    # searches = ['Aluminum alloy','Bronze','Brass','Titanium','AISI']
    searches = ['overview of materials for Bronze']
    material_pages = search_by_keyword(searches=searches,driver= driver, debug= True)
    num_successful_parse = len(material_pages)
    num_failed_parse = 0
    
    folder_location =  os.path.dirname(os.path.abspath(__file__))+'/results_files/'

    try:
        os.mkdir(folder_location)
    except FileExistsError:
        pass

    consecutive_faults = [False, False, False]
    
    iter = 0
    grouping = 10
    grouped_pages = group_lists(material_pages, grouping)
    with click.progressbar(grouped_pages, label= 'Parsing Tables') as bar:
        for pages in bar:
            time.sleep(random.random())

            try:
                matdata_list.append(scrape(pages))
            except Exception:
                exception_msg = 'Issue parsing: ' +'\n'
                num_failed_parse += 1 
                consecutive_faults[iter%3] = True
                print(exception_msg)
                write_to_log(folder_location + 'error_log.txt', exception_msg)
            else:
                consecutive_faults[iter%3] = False
                
            if all(consecutive_faults):
                raise Exception('ERROR: 3 consecutive faults')
            
            iter += 1

    matdata_list = sum(matdata_list, [])
    out_file = '-'.join(searches) + '.yaml'
    out_file = out_file.replace(' ','_')
    write_yaml_file(folder_location + out_file, matdata_list, True)

    driver.quit()
    end = time.time()
    num_successful_parse -= num_failed_parse
    print('Runtime: ', (end-start)/60, 'min')
    print('Successful searches: ', num_successful_parse)
    print('Failed Searches: ', num_failed_parse)