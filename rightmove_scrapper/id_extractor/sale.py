""" Scraper for UK sale property """
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
        print("----------------------Trying to get sale property ids for ", county_name, "----------------------")
        try:
            fixed_price_list = []
            whole_property_ids = []
            price_list = [0, 50000,60000,70000,80000,90000,100000,110000,120000,125000,130000,140000,150000,160000,170000, 175000, 180000,190000,200000,210000,220000,230000,240000,250000,260000,270000,280000,290000,300000,325000,350000,375000,400000,425000,450000,475000,500000,550000,600000,650000,700000,800000,900000,1000000,1250000,1500000,1750000,2000000,2500000,3000000,4000000,5000000,7500000,10000000,15000000, 20000000, 100000000]
            
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
                    url = f"https://www.rightmove.co.uk/property-for-sale/map.html?includeSSTC=false&keywords=&sortType=2&viewType=MAP&channel=BUY&index=0&radius=0.0&locationIdentifier=REGION%{region_code}&minPrice={min_price}&maxPrice={max_price}"
                    
                    if current_min == 20000000:
                        url = f"https://www.rightmove.co.uk/property-for-sale/map.html?includeSSTC=false&keywords=&sortType=2&viewType=MAP&channel=BUY&index=0&radius=0.0&locationIdentifier=REGION%{region_code}&minPrice={current_min}&maxPrice="

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
                                            new_list = self.get_property_ids(f"https://www.rightmove.co.uk/property-for-sale/map.html?includeSSTC=false&keywords=&sortType={sortType}&viewType=MAP&channel=BUY&index=0&radius=0.0&locationIdentifier=REGION%{region_code}&minPrice={max_price}&maxPrice={max_price}&minBedrooms={bedroom_number}")
                                            
                                            property_ids_for_fixed_price_list += new_list
                                        else:
                                            new_list = self.get_property_ids(f"https://www.rightmove.co.uk/property-for-sale/map.html?includeSSTC=false&keywords=&sortType={sortType}&viewType=MAP&channel=BUY&index=0&radius=0.0&locationIdentifier=REGION%{region_code}&minPrice={max_price}&maxPrice={max_price}&minBedrooms={bedroom_number}&maxBedrooms={bedroom_number}")

                                            property_ids_for_fixed_price_list += new_list
                            
                            property_ids_for_fixed_price_list = list(set(property_ids_for_fixed_price_list))
                            whole_property_ids += property_ids_for_fixed_price_list

                            print(f"Special case!- from {min_price} to {max_price}")
                            print(f"Have {len(property_ids_for_fixed_price_list)} for special max price {max_price}")

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
                url = f"https://www.rightmove.co.uk/property-for-sale/map.html?includeSSTC=false&keywords=&sortType=2&viewType=MAP&channel=BUY&index=0&radius=0.0&locationIdentifier=REGION%{region_code}&minPrice={fixed_price}&maxPrice={fixed_price}"
                
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
                                new_list = self.get_property_ids(f"https://www.rightmove.co.uk/property-for-sale/map.html?includeSSTC=false&keywords=&sortType={sortType}&viewType=MAP&channel=BUY&index=0&radius=0.0&locationIdentifier=REGION%{region_code}&minPrice={fixed_price}&maxPrice={fixed_price}&minBedrooms={bedroom_number}")
                                
                                property_ids_for_fixed_price_list += new_list
                                continue
                            else:
                                new_list = self.get_property_ids(f"https://www.rightmove.co.uk/property-for-sale/map.html?includeSSTC=false&keywords=&sortType={sortType}&viewType=MAP&channel=BUY&index=0&radius=0.0&locationIdentifier=REGION%{region_code}&minPrice={fixed_price}&maxPrice={fixed_price}&minBedrooms={bedroom_number}&maxBedrooms={bedroom_number}")

                                property_ids_for_fixed_price_list += new_list

                property_ids_for_fixed_price_list = list(set(property_ids_for_fixed_price_list))
                whole_property_ids += property_ids_for_fixed_price_list

                print(f"Have {len(property_ids_for_fixed_price_list)} for fixed price {fixed_price}")
            
            open(f"../property_id/sale/{country_code}/{county_name}_property_ids.txt", "w").write(str(whole_property_ids))
            open(f"../property_id/sale/id_counts.txt", "a").write(f"Total {len(whole_property_ids)} ids for {county_name}!\n")
            
            print("We have coollected total of", len(whole_property_ids))
            print(f"----------------------Successfully scrape sale property ids for {county_name}----------------------")
        except Exception as e:
            print(f"Error has occured during property_ids for {county_name}", e)
            
if __name__ == "__main__":
    scraper = HouseScraper()
    region_code_dict = {}
    country_code_list = ["sco", "wal"]

    for country_code in country_code_list:
        with open(f"../region_code/{country_code}.txt", "r") as f:  
            region_code_dict = json.load(f)
    
        for key, value in region_code_dict.items():
            county_name = '_'.join(key.lower().split())
            region_code = value
            print("county_name", county_name, "region_code", region_code)
            scraper.get_whole_property_ids(country_code, county_name, region_code)