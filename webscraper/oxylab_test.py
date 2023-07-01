from selenium.webdriver.common.by import By
from seleniumwire import webdriver
import urllib.request
from bs4 import BeautifulSoup
import requests
import time
import aiohttp
import asyncio
# A package to have a chromedriver always up-to-date.

USERNAME = "pcho69"
PASSWORD = "StealthyWebsitePumpk1n"
ENDPOINT = "pr.oxylabs.io:7777"


def chrome_proxy(user: str, password: str, endpoint: str) -> dict:
    wire_options = {
        "proxy": {
            "http": f"http://{user}:{password}@{endpoint}",
            "https": f"http://{user}:{password}@{endpoint}",
        }
    }

    return wire_options

def proxy_2(USERNAME: str, PASSWORD: str):
    entry = ('http://customer-%s:%s@pr.oxylabs.io:7777' %
        (USERNAME, PASSWORD))
    query = {
        'http': entry,
        'https': entry,
    }

    return query

def execute_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    proxies = chrome_proxy(USERNAME, PASSWORD, ENDPOINT)
    driver = webdriver.Chrome( 
       options=options, 
       seleniumwire_options=proxies
    )
    try:
        driver.get("https://ip.oxylabs.io/")
        print(f'\nYour IP is: {driver.find_element(By.CSS_SELECTOR, "pre").text}')
        driver.get("https://ip.oxylabs.io/")
        print(f'\nYour IP is: {driver.find_element(By.CSS_SELECTOR, "pre").text}')
    finally:
        driver.quit()

def execute_urllib_request():
    entry = ('http://customer-%s:%s@pr.oxylabs.io:7777' %
        (USERNAME, PASSWORD))
    query = urllib.request.ProxyHandler({
        'http': entry,
        'https': entry,
    })
    execute = urllib.request.build_opener(query)
    soup = BeautifulSoup(execute.open('https://ip.oxylabs.io').read(),'html.parser')
    print(soup.get_text().strip())

def just_request():
    '''This is the fastest method it seems'''
    for i in range(20):
        proxies = proxy_2(USERNAME, PASSWORD)

        response = requests.get(
            url='https://ip.oxylabs.io',
            proxies= proxies,
            verify=True
        )
        soup = BeautifulSoup(response.content,'lxml')
        print(soup.get_text().strip())

async def fetch(session,url):
    async with session.get(url, proxy = proxy_2(USERNAME, PASSWORD)) as response:
        return await response.text()

async def async_requests():
    async with aiohttp.ClientSession() as session:
        for i in range(10):
            async with session.get(
                    'https://ip.oxylabs.io/',
                    proxy='http://customer-%s:%s@pr.oxylabs.io:7777' % (USERNAME, PASSWORD)
            ) as response:
                content = await response.text()
                soup = BeautifulSoup(content,'lxml')
                print(soup.get_text().strip())


if __name__ == "__main__":
    # sync_start = time.time()
    # just_request()
    # sync_end = time.time()

    async_start = time.time()
    for i in range(2):
        asyncio.run(async_requests())
    async_end = time.time()

    # print('Sync: ', sync_end - sync_start)
    print('Async: ', async_end - async_start)

    # print(just_request())
