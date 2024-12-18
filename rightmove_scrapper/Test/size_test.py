import re
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
    print(size)
    print(conversion_factors.get(unit, 0))
    return size * (conversion_factors.get(unit, 0))  

def extract_area_from_key_features(features):  
    # Regular expression pattern to find numbers followed by units  
    pattern = r"([\d,.]+(?:/\d+)?)(\s?(?:sqm|sq\.?m|sqft|sq\.?ft|ha|sq ft|sq m|acre|\bac\b))"  

    sizes_in_acres = []  

    for feature in features:  
        matches = re.findall(pattern, feature, re.IGNORECASE)  
        for match in matches:  
            size_str, unit = match 
            print(size_str, unit) 
            try:
                size = size_str.replace(',', '')  
            except Exception:
                print("exception")
                continue
            print(size)
            size_in_acres = convert_to_acres(size, unit.lower())  
            print(size_in_acres)
            sizes_in_acres.append(size_in_acres)  

    if sizes_in_acres:  
        return max(sizes_in_acres)  
    return None


def get_size_in_acres(size_list):  
    # Define the priority order for the units  
    priority_order = ['ac', 'sqm', 'sqft', 'ha']  

    # Initialize selected size in acres  
    selected_size_acres = None  

    # Iterate over the priority order and check for each unit  
    for unit in priority_order:  
        for size_info in size_list:  
            if size_info.get('unit') == unit:  
                # Compute the average of minimum and maximum size and convert to acres  
                min_size = Decimal(size_info.get('minimumSize', 0))  
                max_size = Decimal(size_info.get('maximumSize', 0))  
                average_size = (min_size + max_size) / 2  
                selected_size_acres = convert_to_acres(average_size, unit)  
                break  
        if selected_size_acres is not None:  
            break  

    return selected_size_acres 


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
        property_id = "149012540"
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