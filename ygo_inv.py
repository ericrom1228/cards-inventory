import csv
import json
import time
from re import sub
from decimal import Decimal
from selenium import webdriver
from bs4 import BeautifulSoup as bs

def make_json(csvFilePath, jsonFilePath): 
    # create a dictionary 
    data = {} 
      
    # Open a csv reader called DictReader 
    with open(csvFilePath, encoding='utf-8') as csvf: 
        csvReader = csv.DictReader(csvf) 
          
        # Convert each row into a dictionary  
        # and add it to data 
        for rows in csvReader: 
              
            # Assuming a column named 'No' to 
            # be the primary key 
            key = rows['Card Name'] 
            data[key] = rows 
  
    # Open a json writer, and use the json.dumps()  
    # function to dump data 
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf: 
        jsonf.write(json.dumps(data, indent=4)) 
          

def get_card_id_list():
    with open("inventory_list_copy.csv") as ygo_list:
        lines = ygo_list.readlines()
        headers = lines[0]
        card_id_list = []
        for line in lines[1:]:
            line = line.split(",")
            card_id_list.append(line[0])

    return card_id_list
    

def get_max_card_value(search_string):
    browser = webdriver.Chrome()

    url = "https://mavin.io/search?q=" + search_string + "&bt=sold#"
    #print("url", url)
    browser.get(url)

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
    browser.close()

    # Throw your source into BeautifulSoup and start parsing!
    bs_data = bs(source_data, features="lxml")

    price_list = bs_data.select("h3.sold-price")
    price_list = [Decimal(sub(r'[^\d.]', '', price["data-sold"])) for price in price_list]

    if price_list:
        #print("max possible value: ", max(price_list))
        max_card_value = str(max(price_list))
        return max_card_value
    else:
        #print("no available value")
        return("no available value")

def write_max_card_value(max_card_value, index):
    with open("inventory_list_copy.csv","r") as ygo_list:
        lines = ygo_list.readlines()
        headers = lines[0]
        lines = lines[1:]

    lines[index] = lines[index].split(",")
    lines[index][6] = max_card_value
    lines[index].append('\n')
    lines[index] = ','.join(lines[index])

    lines.insert(0, headers)

    with open("inventory_list_copy.csv","w") as new_ygo_list:
        new_ygo_list.writelines(lines)

#csvFilePath = r'inventory_list_copy.csv'
#jsonFilePath = r'inventory_list.json'
#make_json(csvFilePath, jsonFilePath)

##### for just one entry #####
#card_id = "CT1-EN001"
#print(card_id)
#print(get_max_card_value(card_id))
#write_max_card_value(get_max_card_value(card_id))
#write_max_card_value(1)

##### for the full list ######
card_id_list = get_card_id_list()
i = 0
max_card_value_list = []
for card_id in card_id_list:
    print(card_id)
    max_card_value = get_max_card_value(card_id)
    print(max_card_value)
    write_max_card_value(max_card_value, i)
    i += 1
    max_card_value_list.append(max_card_value)
    print(max_card_value_list)