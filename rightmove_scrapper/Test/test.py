import json
import re
from fractions import Fraction 

import csv
import asyncio

from typing import List
from bs4 import BeautifulSoup
from httpx import AsyncClient, Response
from parsel import Selector

# 1. establish HTTP client with browser-like headers to avoid being blocked
client = AsyncClient(
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,lt;q=0.8,et;q=0.7,de;q=0.6",
    },
    follow_redirects=True,
    http2=True,  # enable http2 to reduce block chance
    timeout=30,
)

def clean_html(html_content):  
    # Parse the HTML content  
    soup = BeautifulSoup(html_content, 'html.parser')  
    # Extract text and return  
    return soup.get_text(separator='\n')  

def extract_property(response: Response) -> dict:
    """extract property data from rightmove PAGE_MODEL javascript variable"""
    selector = Selector(response.text)
    data = selector.xpath("//script[contains(.,'PAGE_MODEL = ')]/text()").get()
    if not data:
        print(f"page {response.url} is not a property listing page")
        return
    data = data.split("PAGE_MODEL =", 1)[1].strip()  
    data = data.split("window.adInfo =", 1)[0].strip()  

    with open("data.txt", "w") as f:
        f.write(data)
    

    # Parse the JSON string into a Python dictionary  
    json_data = json.loads(data)  
    
    # Access and return the 'propertyData' key  
    return json_data["propertyData"]

# this is our main scraping function that takes urls and returns the data
async def scrape_properties(urls: List[str]) -> List[dict]:
    properties = []
    try:
        """Scrape Rightmove property listings for property data"""
        to_scrape = [client.get(url) for url in urls]
        for response in asyncio.as_completed(to_scrape):
            response = await response
            properties.append(extract_property(response))
    except Exception as e:
        print("Error has occured during scraping properties", e)
    return properties

def convert_to_acres(size, unit):  
    """Converts a given size from a specified unit to acres."""  
    conversion_factors = {  
        'sqm': 0.000247105,  
        'sq.m': 0.000247105,  
        'sq m': 0.000247105, 
        'sqft': 0.0000229568,  
        'sq.ft': 0.0000229568,  
        'sq ft': 0.0000229568, 
        'ha': 2.47105,  
        'ac': 1,  
        'acre': 1  
    }  
    return size * (conversion_factors.get(unit, 0))  


def extract_size_and_unit(text):  
    text = text.replace(',', '')
    # Helper function to convert fraction strings to float  
    def handle_fraction(num):  
        if '/' in num:  
            try:  
                return str(float(Fraction(num)))  
            except ZeroDivisionError:  
                return None  
        return num  

    # Pattern matching for valid sizes and units  
    patterns = [
        (r'(?<![\w.])(-?[\d,]+(?:/\d+)?(?:\.\d+)?)\s*(acs|acre|ac|Ac|Acs|Acre|acres|Acres)\b', 'acre'),  
        (r'(?<![\w.])(-?[\d,]+(?:/\d+)?(?:\.\d+)?)\s*(sq\.?\s*ms|sqm|sq\.m|sqms|sq m|sq meter|sq meters|sq Meter|sq Meters|square meter|square meters|square Meter|square Meters)\b', 'sqm'),  
        (r'(?<![\w.])(-?[\d,]+(?:/\d+)?(?:\.\d+)?)\s*(sq\.?\s*fts|sqft|sq\.ft|sqfts|sq ft|sq feet|sq feets|square feet|square feets|sq Feet|sq Feets|square Feet|square Feets)\b', 'sqft'),  
        (r'(?<![\w.])(-?[\d,]+(?:/\d+)?(?:\.\d+)?)\s*(ha|Ha|Hectare|Hectares|hectar|hectares)\b', 'ha')  
    ]
    
    if '"' in text:  
        return None, None  
    
    for pattern, unit in patterns:  
        match = re.search(pattern, text)  
        if match:  
            print(match)
            number_str = match.group(1)  
            # Remove commas and handle fractions  
            number_str = number_str.replace(',', '')  
            number = handle_fraction(number_str)  
            if number is not None:  
                return number, unit  
    
    return None, None  

def extract_area_from_key_features(features):  
    sizes_in_acres = []  
    print("len(features)",len(features))
    for feature in features:  
        size, unit = extract_size_and_unit(feature)
        if size is not None and unit is not None:
            print("feature", feature)
            print("size, unit",size, unit)
            size_in_acre = convert_to_acres(float(size), unit)
            sizes_in_acres.append(size_in_acre)

    print("sizes_in_acres",sizes_in_acres)
    if sizes_in_acres:  
        return max(sizes_in_acres)  
    return None

def get_size_in_acres(size_list):
    print("size_list",size_list)
    # Define the priority order for the units  
    priority_order = ['ac', 'sqm', 'sqft', 'ha']  

    # Initialize selected size in acres  
    selected_size_acres = None

    # Iterate over the priority order and check for each unit  
    for unit in priority_order:  
        for size_info in size_list:  
            if size_info.get('unit') == unit:  
                # Compute the average of minimum and maximum size and convert to acres  
                min_size = size_info.get('minimumSize', 0)  
                max_size = size_info.get('maximumSize', 0)  
                print("min_size, max_size",min_size, max_size)
                average_size = (min_size + max_size) / 2  
                selected_size_acres = convert_to_acres(average_size, unit)  
                break  
        if selected_size_acres is not None:  
            break  

    return selected_size_acres 

def get_size(property_dict):  
    actual_size = 0  
    property_size, feature_size = 0, 0  
    
    if property_dict[0]:     
        try:   
            property_size = property_dict[0]["sizings"]  
            property_size = get_size_in_acres(property_size) or 0  # Default to 0 if None  
        except Exception:  
            pass

        try:  
            feature_size = extract_area_from_key_features(property_dict[0]["keyFeatures"]) or 0  # Default to 0 if None  
        except Exception:  
            pass  
    print("property_size", property_size)
    print("feature_size", feature_size)
    # Use max with default values to safely compare  
    if property_size == 0 and feature_size == 0:  
        actual_size = 0  
    else:  
        actual_size = max(property_size if property_size is not None else 0,   
                          feature_size if feature_size is not None else 0)  
    if actual_size == 0:
        return "Not listed on Page. Ask Agent!"
    actual_size = "{:.4f}".format(actual_size)  
    return actual_size

def append_dict_to_csv(data, file_path):  
    # Function to flatten a dictionary for CSV writing  
    def flatten_dict(data):  
        flattened_item = {}  
        for key, value in data.items():  
            if isinstance(value, list):  
                # Join list items into a string for CSV format  
                flattened_item[key] = ', '.join(value)  
            else:  
                flattened_item[key] = value  
        return flattened_item  

    # Flatten the input dictionary  
    flattened_data = flatten_dict(data)  

    # Write data to the specified CSV file  
    with open(file_path, mode='a+', newline='') as file:  
        # Move file cursor to the start for initial check  
        file.seek(0)  
        first_char = file.read(1)  
        
        writer = csv.DictWriter(file, fieldnames=flattened_data.keys())  
        
        # Write header if the file is new or empty  
        if not first_char:  
            writer.writeheader()  
        
        # Ensure cursor is at the end for appending new data  
        file.seek(0, 2)  
        writer.writerow(flattened_data)  

def get_detailed_info(i, property_list):
    id = property_list[0]["id"]
    link_to_property = f"https://www.rightmove.co.uk/properties/{id}#/"
    price = property_list[0]["prices"]["primaryPrice"].replace("£", "").replace(",", "")  
    size = get_size(property_list)
    key_features = ""
    for index, element in enumerate(property_list[0]["keyFeatures"]):  
        key_features += str(f"{index + 1}. {element} | ")
    address = property_list[0]["address"]["displayAddress"]
    description = property_list[0]["text"]["description"]
    description = clean_html(description)
    agent_name = property_list[0]["customer"]["companyName"]
    agent_address = property_list[0]["customer"]["displayAddress"].replace("\n", "").replace("\r", "")
    agent_contact_url = "https://www.rightmove.co.uk/" + str(property_list[0]["customer"]["valuationFormUrl"])
    
    property_dict = {
        "No.": i,
        "id": id,
        "link_to_property": link_to_property,
        "price": price,
        "size": size,
        "address": address,
        "key_features": key_features,
        "description": description,
        "agent_name": agent_name,
        "agent_address": agent_address,
        "agent_contact_url": agent_contact_url
    }

    append_dict_to_csv(property_dict, f"rightmove_data_second.csv")

# Eexample run:
async def run():
    not_found_list2 = []
    all_lists = []
    country_code_list = ["eng", "sco", "wal", "nir"]
    # for country_code in country_code_list:
    #     folder_path = f"property_id/sale/{country_code}"
    #     for filename in os.listdir(folder_path):
    #         file_path = os.path.join(folder_path, filename)  
            
    #         # Check if it's a file (to avoid directories)  
    #         if os.path.isfile(file_path):
    #             # Open the file and read the data  
    #             with open(file_path, 'r') as file:  
    #                 try:  
    #                     data_list = json.load(file)  # Assuming the file contains a JSON list 
    #                     print(len(data_list))
    #                     all_lists.extend(data_list)  
    #                 except json.JSONDecodeError as e:
    #                     print(f"Could not decode JSON from file {filename}: {e}")  
    
        
    # all_lists = list(set(all_lists))
    # with open("all_lists.txt", "w") as f:
    #     f.write(str(all_lists))
    # file_path = 'all_lists.txt'  

    # # Open and read the file  
    # with open(file_path, 'r') as file:  
    #     content = file.read()  

    # # Safely evaluate the content to convert it into a Python list  
    # all_lists = ast.literal_eval(content)
    # print("number of unique properties: ",len(all_lists))
    # midpoint = len(all_lists) // 2  
    # # Split the list into two parts  
    # first_half = all_lists[:midpoint]  
    # second_half = all_lists[midpoint:] 
    # for index, property_id in enumerate(second_half):
    try:
        property_id = "150080288"
        property_data = await scrape_properties([f"https://www.rightmove.co.uk/properties/{property_id}#/"])
        # if property_data == []:
        #     print(f"Error occurred while scraping property {property_id}: {e}")
        #     not_found_list2.append(property_id)
        #     continue

        print(get_size(property_data))
    except Exception as e:
        print(f"Error occurred while scraping id {property_id}: {e}")
        # not_found_list2.append(property_id)
        
    # with open("not_found_list2.txt", "w") as f:
    #     f.write(str(not_found_list2))
if __name__ == "__main__":
    asyncio.run(run())