from undetected_chromedriver import Chrome
import time
from bs4 import BeautifulSoup
import json
import pandas as pd
# create a new instance of Chrome
chrome = Chrome()
all_urls = []
def clean_url(url):
    # Remove everything after and including '?'
    return url.split('?')[0]
def extract_id(url):
    # Split the URL by '/' and get the second-to-last segment
    return url.strip('/').split('/')[-1]


url = input("Enter the url : ") 
update_url = url + '&pn=1'
chrome.get(update_url)
chrome.find_element('xpath','//button[@id="onetrust-accept-btn-handler"]').click()
soup = BeautifulSoup(chrome.page_source, 'html.parser')
elements = soup.find_all('a', class_='_1lw0o5c1')  # Adjust the class as needed
urls = ['https://www.zoopla.co.uk/'+ element.get('href') for element in elements if element.get('href')]
cleaned_urls = [clean_url(url) for url in urls]
for url in cleaned_urls:
    chrome.get(url)
    time.sleep(2)
    try:
        price = chrome.find_element('xpath','//p[@class="_194zg6t3 r4q9to1"]').text.replace('£','')
    except:
        price = None
    print(price)
    try:
        bed = chrome.find_element('xpath','//p[contains(@class, "_194zg6t8") and contains(@class, "_1wmbmfq3") and contains(text(), "bed")]').text
    except:
        bed = None
    try:
        bath = chrome.find_element('xpath','//p[contains(@class, "_194zg6t8") and contains(@class, "_1wmbmfq3") and contains(text(), "bath")]').text
    except:
        bath = None
    try:
        area = chrome.find_element('xpath','//p[contains(@class, "_194zg6t8") and contains(@class, "_1wmbmfq3") and contains(text(), "sq.")]').text
    except:
        area = None
    try:
        address = chrome.find_element('xpath','//address[@class="_1olqsf99"]').text
    except:
        address = None    
    try:
        agent_name = chrome.find_element('xpath','//p[@class="_194zg6t7 _133vwz72"]').text
    except:
        agent_name = None
    try:
        key_features_elements = chrome.find_elements('xpath','//p[@class="_15a8ens2"]/span')
        key_features_texts = [element.text for element in key_features_elements if element.text.strip()]
    except:
        key_features_texts = None
    d = {
        'id': extract_id(url),
        'url':url,
        'price':price,
        'bed':bed,
        'bath':bath,
        'size':area,
        'address':address,
        'key_features':key_features_texts,
        'description':None,
        'agent_name':agent_name,
        'agent_address':None,
        'contact_url':None
        

    }
    #chrome.close()
    print(d)
    #break
    time.sleep(3)
    
chrome.close()

#while True:
#    pages = chrome.find_elements('xpath','//a[@class="qimhss5 qimhss8 qimhsse qimhss0 qimhss2 _194zg6t8"]/@href')
#    last = pages[-1].get_attribute('href')
#    chrome.get(last)
       


