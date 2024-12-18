""" Scraper for UK rent property """
import re
import json  
import requests
from bs4 import BeautifulSoup  

class HouseScraper():
    def get_property_ids(self, url):        
        res = requests.get(url)        
        soup = BeautifulSoup(res.text, 'html.parser')
        script_tag = soup.find('script', text=re.compile('window\\.jsonModel'))
        
        if script_tag:
            script_content = script_tag.string
            property_ids = re.findall(r'"id"\s*:\s*(\d+),\s*"location"', script_content)
            property_ids = list(map(int, property_ids)) 

            return property_ids[:-1]
        else:
            print("Could not find the targeted script tag.")
            return []

    def get_whole_property_ids(self, country_code, county_name, region_code):
        print("----------------------Trying to get rent property ids for ", county_name, "-----------------------")
        try:
            fixed_price_list = []
            whole_property_ids = []
            price_list = [1, 100, 150, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1250, 1300, 1400, 1500, 1750, 2000, 2250, 2500, 2750, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 8000, 9000, 10000, 12500, 15000, 17500, 20000, 25000, 30000, 35000, 40000, 100000000]

            for i in range(len(price_list) - 2):
                min_price = price_list[i]
                max_price = price_list[i + 1]  
                ranges_to_check = [(min_price, max_price)]  

                fixed_price_list.append(min_price)
                fixed_price_list.append(max_price)
                
                while ranges_to_check:  
                    current_min, current_max = ranges_to_check.pop(0)
                    min_price = current_min + 1
                    max_price = current_max -1

                    url = f"https://www.rightmove.co.uk/property-to-rent/map.html?locationIdentifier=REGION%{region_code}&maxPrice={max_price}&minPrice={min_price}&numberOfPropertiesPerPage=499&propertyTypes=&includeLetAgreed=false&viewType=MAP&mustHave=&dontShow=&furnishTypes=&keywords="
                    
                    if current_min == 40000:
                        url = f"https://www.rightmove.co.uk/property-to-rent/map.html?locationIdentifier=REGION%{region_code}&minPrice={min_price}&numberOfPropertiesPerPage=499&propertyTypes=&includeLetAgreed=false&viewType=MAP&mustHave=&dontShow=&furnishTypes=&keywords="

                    property_ids = self.get_property_ids(url)
                
                    if len(property_ids) < 498:
                        print(f"Perform operation on range: ({min_price}, {max_price}) with {len(property_ids)} IDs")
                        whole_property_ids += property_ids
                    else:
                        if max_price <= min_price:
                            if max_price not in fixed_price_list:
                                sortType_list = [1, 2, 6, 10]
                                bedroom_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                                property_ids_for_fixed_price_list = []
                                new_list = []
                                for sortType in sortType_list:
                                    for bedroom_number in bedroom_list:
                                        if bedroom_number == 10:
                                            new_list = self.get_property_ids(f"https://www.rightmove.co.uk/property-to-rent/map.html?locationIdentifier=REGION%{region_code}&minBedrooms={bedroom_number}&maxPrice={max_price}&propertySearchType=RENT&minPrice={min_price}&numberOfPropertiesPerPage=499&sortType={sortType}&propertyTypes=&includeLetAgreed=false&viewType=MAP&mustHave=&dontShow=&furnishTypes=&keywords=")
                                            
                                            property_ids_for_fixed_price_list += new_list
                                        else:
                                            new_list = self.get_property_ids(f"https://www.rightmove.co.uk/property-to-rent/map.html?locationIdentifier=REGION%{region_code}&minBedrooms={bedroom_number}&mBedrooms={bedroom_number}&maxPrice={max_price}&propertySearchType=RENT&minPrice={min_price}&numberOfPropertiesPerPage=499&sortType={sortType}&propertyTypes=&includeLetAgreed=false&viewType=MAP&mustHave=&dontShow=&furnishTypes=&keywords=")

                                            property_ids_for_fixed_price_list += new_list
                            
                            property_ids_for_fixed_price_list = list(set(property_ids_for_fixed_price_list))
                            whole_property_ids += property_ids_for_fixed_price_list
                            print(f"Special case!- min_price {min_price}, max_price {max_price}")
                            print(f"Have {len(property_ids_for_fixed_price_list)} for special case!")

                        else:
                            mid_point = (current_min + current_max) // 2
                            ranges_to_check.append((current_min, mid_point))
                            ranges_to_check.append((mid_point, current_max))
                            
                            fixed_price_list.append(current_min)
                            fixed_price_list.append(current_max)
                            fixed_price_list.append(mid_point)

            fixed_price_list = list(set(fixed_price_list))

            remove_list = [0, 100000000]

            for i in remove_list:
                if i in fixed_price_list:
                    fixed_price_list.remove(i)
                    
            print("fixed price list", fixed_price_list)

            for fixed_price in fixed_price_list:
                url = f"https://www.rightmove.co.uk/property-to-rent/map.html?locationIdentifier=REGION%{region_code}&maxPrice={fixed_price}&propertySearchType=RENT&minPrice={fixed_price}&numberOfPropertiesPerPage=499&sortType=2&propertyTypes=&includeLetAgreed=false&viewType=MAP&mustHave=&dontShow=&furnishTypes=&keywords="
                
                property_ids_for_fixed_price_list = []
                property_ids_for_fixed_price_list = self.get_property_ids(url)
                if len(property_ids_for_fixed_price_list) >= 498:  
                    sortType_list = [1, 2, 6, 10]
                    bedroom_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                    property_ids_for_fixed_price_list = []
                    new_list = []
                    for sortType in sortType_list:
                        for bedroom_number in bedroom_list:
                            if bedroom_number == 10:
                                new_list = self.get_property_ids(f"https://www.rightmove.co.uk/property-to-rent/map.html?locationIdentifier=REGION%{region_code}&maxPrice={fixed_price}&propertySearchType=RENT&minPrice={fixed_price}&minBedrooms={bedroom_number}&numberOfPropertiesPerPage=499&sortType={sortType}&propertyTypes=&includeLetAgreed=false&viewType=MAP&mustHave=&dontShow=&furnishTypes=&keywords=")
                                
                                property_ids_for_fixed_price_list += new_list
                                continue
                            else:
                                new_list = self.get_property_ids(f"https://www.rightmove.co.uk/property-to-rent/map.html?locationIdentifier=REGION%{region_code}&maxPrice={fixed_price}&propertySearchType=RENT&minPrice={fixed_price}&minBedrooms={bedroom_number}&maxBedrooms={bedroom_number}&numberOfPropertiesPerPage=499&sortType={sortType}&propertyTypes=&includeLetAgreed=false&viewType=MAP&mustHave=&dontShow=&furnishTypes=&keywords=")

                                property_ids_for_fixed_price_list += new_list

                property_ids_for_fixed_price_list = list(set(property_ids_for_fixed_price_list))
                whole_property_ids += property_ids_for_fixed_price_list
                print(f"Have {len(property_ids_for_fixed_price_list)} for fixed price {fixed_price}")

            open(f"../property_id/rent/{country_code}/{county_name}_property_ids.txt", "w").write(str(whole_property_ids))
            open(f"../property_id/rent/id_counts.txt", "a").write(f"Total {len(whole_property_ids)} ids for {county_name}!\n")

            print("We have coollected total of", len(whole_property_ids))
            print(f"----------------------Successfully scrape rent property ids for {county_name}----------------------")
        except Exception as e:
            print(f"Error has occured during property_ids for {county_name}", e)

if __name__ == "__main__":
    scrapper = HouseScraper()
    region_code_dict = {}  
    country_code_list = ["sco", "wal"]

    for country_code in country_code_list:
        with open(f"../region_code/{country_code}.txt", "r") as f:  
            region_code_dict = json.load(f)
    
        for key, value in region_code_dict.items():
            county_name = '_'.join(key.lower().split())
            region_code = value
            print("county_name", county_name, "region_code", region_code)
            scrapper.get_whole_property_ids(country_code, county_name, region_code)
            