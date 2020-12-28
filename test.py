import time
from re import sub
from decimal import Decimal
from selenium import webdriver
from bs4 import BeautifulSoup as bs

browser = webdriver.Chrome()
browser.get("https://mavin.io/search?q=CT1-EN001&bt=sold#")

# Selenium script to scroll to the bottom, wait 3 seconds for the next batch of data to load, then continue scrolling.  It will continue to do this until the page stops loading new data.
lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
match=False
while(match==False):
    lastCount = lenOfPage
    time.sleep(3)
    lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    if lastCount==lenOfPage:
        match=True

# Now that the page is fully scrolled, grab the source code.
source_data = browser.page_source

# Throw your source into BeautifulSoup and start parsing!
bs_data = bs(source_data, features="lxml")
#print("type(bs_data)", type(bs_data))

price_list = bs_data.select("h3.sold-price")
price_list = [Decimal(sub(r'[^\d.]', '', price["data-sold"])) for price in price_list]

if price_list:
    print("max possible value: ", max(price_list))
else:
    print("no available value")

browser.close()