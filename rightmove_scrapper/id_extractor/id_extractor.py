from bs4 import BeautifulSoup  
import re  
import requests

sale_url = "https://www.rightmove.co.uk/property-for-sale/map.html?areaSizeUnit=sqft&channel=BUY&currencyCode=GBP&locationIdentifier=USERDEFINEDAREA%5E%7B%22polylines%22%3A%22srwqIphng%40rmsCtjmGjdbA%7CtrApvbAedwBbmTyh%60Fvj%5DimiIy%7C%7BCr_NupuAddwBanyA%7CtrA%7Be%40%7C~eB%22%7D&mustHave=&propertyTypes=&radius=0.0&sortType=2&viewType=MAP"
rent_url = "https://www.rightmove.co.uk/property-to-rent/map.html?areaSizeUnit=sqft&channel=RENT&currencyCode=GBP&locationIdentifier=USERDEFINEDAREA%5E%7B%22polylines%22%3A%22kvxpIz%7D%7Bi%40hu%7DBlsbGrp%7CAs_Nx%7DpAsfaKcvP%7BnyCk%60wAgxv%40oxnBff%7D%40yavA%7Cj_AatBvrsFbbE_iR%22%7D&mustHave=&propertyTypes=&radius=0.0&sortType=2&viewType=MAP"
url = "https://www.rightmove.co.uk/property-for-sale/map.html?locationIdentifier=REGION%5E87490&maxPrice=550000&minPrice=550000&edit=true"
res = requests.get(url)
with open("result.txt", "w") as f:
    f.write(res.text)

soup = BeautifulSoup(res.text, 'html.parser')  

# Find the script tag containing window.jsonModel  
script_tag = soup.find('script', text=re.compile('window\\.jsonModel'))  

if script_tag:
    script_content = script_tag.string  

    # Use regex to find all property IDs  
    property_ids = re.findall(r'"id"\s*:\s*(\d+),\s*"location"', script_content)
    property_ids = list(map(int, property_ids))  # Convert string IDs to integers  

    print(property_ids[:-1])  
    print(len(property_ids[:-1]))
else:
    print("Could not find the targeted script tag.")