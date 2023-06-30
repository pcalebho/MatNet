from selenium.webdriver.common.by import By
from seleniumwire import webdriver
import urllib.request
from bs4 import BeautifulSoup
import requests
import time
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
    print(soup.get_text())

def just_request():
    proxies = chrome_proxy(USERNAME, PASSWORD, ENDPOINT)

    response = requests.get(
        url='https://ip.oxylabs.io',
        proxies=proxies,
        verify=True
    )
    soup = BeautifulSoup(response.content,'html.parser')
    print(soup.get_text())



if __name__ == "__main__":
    # execute_driver()
    

    start = time.time()
    just_request()
    print('request: ', time.time()-start)

    start = time.time()
    execute_urllib_request()
    print('URLlib_runtime: ', time.time()-start)