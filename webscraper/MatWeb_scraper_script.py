import requests
from bs4 import BeautifulSoup
import pandas as pd

searches = ['AISI']

url = 'https://matweb.com/search/QuickText.aspx?SearchText=' + searches[0]
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

next_page_id='ctl00_ContentMain_ucSearchResults1_lnkNextPage'
material_pages_link_id = 'lnkMatl'
print(soup.prettify())