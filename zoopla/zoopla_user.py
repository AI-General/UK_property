from undetected_chromedriver import Chrome
import time
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# Create a new instance of Chrome
chrome = Chrome()
all_urls = []
data = []

def clean_url(url):
    return url.split('?')[0]

def extract_id(url):
    return url.strip('/').split('/')[-1]

# Get user input for the URL and number of pages to scrape
url = "https://www.zoopla.co.uk/for-sale/property/oxford/?q=Oxford&results_sort=newest_listings&search_source=home"

page_number = 0

while True:
    page_number += 1
    # Update the URL with the current page number
    update_url = url + f'&pn={page_number}'
    
    # Print the current page number for monitoring
    print(f"Scraping page {page_number}: {update_url}")
    
    chrome.get(update_url)
    time.sleep(3)

    try:
        chrome.find_element('xpath', '//button[@id="onetrust-accept-btn-handler"]').click()
    except:
        pass

    soup = BeautifulSoup(chrome.page_source, 'html.parser')
    elements = soup.find_all('a', class_='_1lw0o5c1')
    urls = ['https://www.zoopla.co.uk' + element.get('href') for element in elements if element.get('href')]
    cleaned_urls = [clean_url(url) for url in urls]

    if not cleaned_urls:
        print("No more listings found. Exiting pagination.")
        break

    for url in cleaned_urls:
        chrome.get(url)
        time.sleep(2)

        bath_xpath = '(//p[contains(text(),"bath")])[1] |  (//div[contains(text(),"bath")])[1]'  
        bed_xpath = '(//p[contains(text(),"bed")])[1] |  (//div[contains(text(),"bed")])[1]'  
        size_xpath = '(//p[contains(text(),"sq")])[1] |  (//div[contains(text(),"sq")])[1]'  

        try:
            price = chrome.find_element('xpath', '(//p[contains(text(),"£")])[1]').text.replace('£', '')
        except:
            price = None

        try:
            bed = chrome.find_element('xpath', bed_xpath).text
        except:
            bed = None

        try:
            bath = chrome.find_element('xpath', bath_xpath).text
        except:
            bath = None

        try:
            area = chrome.find_element('xpath', size_xpath).text
        except:
            area = None

        try:
            address = chrome.find_element('xpath', '//address[@class="_1olqsf99"]').text
        except:
            address = None

        try:
            agent_name = chrome.find_element('xpath', '//p[@class="_194zg6t7 _133vwz72"]').text
        except:
            agent_name = None

        try:
            key_features_elements = chrome.find_elements('xpath', '//p[@class="_15a8ens2"]/span')
            key_features_texts = [element.text for element in key_features_elements if element.text.strip()]
        except:
            key_features_texts = None

        xpath_combined = '//div/a[contains(@href, "find-agents")] | //div/a[contains(@href, "developers")]'
        try:
            agent_url = chrome.find_element('xpath', xpath_combined).get_attribute('href')
        except:
            agent_url = None

        if agent_url:
            chrome.get(agent_url)
            time.sleep(2)
            try:
                agent_address = chrome.find_element('xpath', '(//div[@class="_1o3tb3f0"]/p)[1]').text
            except:
                agent_address = None

            try:
                agent_phone = chrome.find_element('xpath', '((//div[@class="_1o3tb3f0"]/p)[2]/a)[1]').get_attribute('aria-label').replace('Call ', '')
            except:
                agent_phone = None
        else:
            agent_address = None
            agent_phone = None

        d = {
            'id': extract_id(url),
            'url': url,
            'price': price,
            'bed': bed,
            'bath': bath,
            'size': area,
            'address': address,
            'key_features': key_features_texts,
            'agent_name': agent_name,
            'agent_address': agent_address,
            'phone': agent_phone
        }
        data.append(d)
        print(d)
        time.sleep(1)

    # Increment the page number for the next iteration
    page_number += 1

# Close the browser
chrome.close()

# Export data to CSV
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M")
csv_filename = f"export_{current_time}.csv"
df = pd.DataFrame(data)
df.to_csv(csv_filename, index=False)
print(f"Data exported to {csv_filename}")