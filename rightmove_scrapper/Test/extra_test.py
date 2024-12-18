import re  
from fractions import Fraction  

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
        (r'(?<![\w.])(-?[\d,]+(?:/\d+)?(?:\.\d+)?)\s*(sq\.?\s*ms|sqm|sq\.m|sqms|sq m)\b', 'sqm'),  
        (r'(?<![\w.])(-?[\d,]+(?:/\d+)?(?:\.\d+)?)\s*(sq\.?\s*fts|sqft|sq\.ft|sqfts|sq ft)\b', 'sqft'),  
        (r'(?<![\w.])(-?[\d,]+(?:/\d+)?(?:\.\d+)?)\s*(ha|Ha|Hectare|Hectares|hectar|hectares)\b', 'ha')  
    ]  
    
    if '"' in text:  
        return False  
    
    for pattern, unit in patterns:  
        match = re.search(pattern, text)  
        if match:  
            print(match)
            number_str = match.group(1)  
            # Remove commas and handle fractions  
            number_str = number_str.replace(',', '')  
            number = handle_fraction(number_str)  
            if number is not None:  
                return f"{number} {unit}"  
    
    return False  

# Examples of how to use this function  
texts = [  
    "2 bedroom",  
]  
test_cases = [  
    "apple 12.5 ac tomato",  
    "apple 12.5 actomato",  
    "apple 12.5ac tomato",  
    "apple 12.5actomato",  
    "apple pear12.5 ac tomato",  
    "apple pear12.5 actomato",  
    "apple pear12.5ac tomato",  
    "apple pear12.5actomato",  
    
    "apple 12.5 Ac tomato",  
    "apple 12.5 Actomato",  
    "apple 12.5Ac tomato",  
    "apple 12.5Actomato",  
    "apple pear12.5 Ac tomato",  
    "apple pear12.5 Actomato",  
    "apple pear12.5Ac tomato",  
    "apple pear12.5Actomato",  
    
    "apple 12.5 Acre tomato",  
    "apple 12.5 Acretomato",  
    "apple 12.5Acre tomato",  
    "apple 12.5Acretomato",  
    "apple pear12.5 Acre tomato",  
    "apple pear12.5 Acretomato",  
    "apple pear12.5Acre tomato",  
    "apple pear12.5Acretomato",  
    
    "apple 12.5 acs tomato",  
    "apple 12.5 acstomato",  
    "apple 12.5acs tomato",  
    "apple 12.5acstomato",  
    "apple pear12.5 acs tomato",  
    "apple pear12.5 acstomato",  
    "apple pear12.5acs tomato",  
    "apple pear12.5acstomato",  
    
    "apple 12.5 acres tomato",  
    "apple 12.5 acrestomato",  
    "apple 12.5acres tomato",  
    "apple 12.5acrestomato",  
    "apple pear12.5 acres tomato",  
    "apple pear12.5 acrestomato",  
    "apple pear12.5acres tomato",  
    "apple pear12.5acrestomato",  
    
    "apple 12.5 acre tomato",  
    "apple 12.5 acretomato",  
    "apple 12.5acre tomato",  
    "apple 12.5acretomato",  
    "apple pear12.5 acre tomato",  
    "apple pear12.5 acretomato",  
    "apple pear12.5acre tomato",  
    "apple pear12.5acretomato",  
    
    "apple 12.5 Acs tomato",  
    "apple 12.5 Acstomato",  
    "apple 12.5Acs tomato",  
    "apple 12.5Acstomato",  
    "apple pear12.5 Acs tomato",  
    "apple pear12.5 Acstomato",  
    "apple pear12.5Acs tomato",  
    "apple pear12.5Acstomato",  
    
    "apple 12.5 sqm tomato",  
    "apple 12.5 sqmtomato",  
    "apple 12.5sqm tomato",  
    "apple 12.5sqmtomato",  
    "apple pear12.5 sqm tomato",  
    "apple pear12.5 sqmtomato",  
    "apple pear12.5sqm tomato",  
    "apple pear12.5sqmtomato",  
    
    "apple 12.5 sq.m tomato",  
    "apple 12.5 sq.mtomato",  
    "apple 12.5sq.m tomato",  
    "apple 12.5sq.mtomato",  
    "apple pear12.5 sq.m tomato",  
    "apple pear12.5 sq.mtomato",  
    "apple pear12.5sq.m tomato",  
    "apple pear12.5sq.mtomato",  
    
    "apple 12.5 sqms tomato",  
    "apple 12.5 sqmstomato",  
    "apple 12.5sqms tomato",  
    "apple 12.5sqmstomato",  
    "apple pear12.5 sqms tomato",  
    "apple pear12.5 sqmstomato",  
    "apple pear12.5sqms tomato",  
    "apple pear12.5sqmstomato",  
    
    "apple 12.5 sq ms tomato",  
    "apple 12.5 sq mstomato",  
    "apple 12.5sq ms tomato",  
    "apple 12.5sq mstomato",  
    "apple pear12.5 sq ms tomato",  
    "apple pear12.5 sq mstomato",  
    "apple pear12.5sq ms tomato",  
    "apple pear12.5sq mstomato",  
    
    "apple 12.5 sq.ms tomato",  
    "apple 12.5 sq.mstomato",  
    "apple 12.5sq.ms tomato",  
    "apple 12.5sq.mstomato",  
    "apple pear12.5 sq.ms tomato",  
    "apple pear12.5 sq.mstomato",  
    "apple pear12.5sq.ms tomato",  
    "apple pear12.5sq.mstomato",  
    
    "apple 12.5 sqft tomato",  
    "apple 12.5 sqfttomato",  
    "apple 12.5sqft tomato",  
    "apple 12.5sqfttomato",  
    "apple pear12.5 sqft tomato",  
    "apple pear12.5 sqfttomato",  
    "apple pear12.5sqft tomato",  
    "apple pear12.5sqfttomato",  
    
    "apple 12.5 sq.ft tomato",  
    "apple 12.5 sq.fttomato",  
    "apple 12.5sq.ft tomato",  
    "apple 12.5sq.fttomato",  
    "apple pear12.5 sq.ft tomato",  
    "apple pear12.5 sq.fttomato",  
    "apple pear12.5sq.ft tomato",  
    "apple pear12.5sq.fttomato",  
    
    "apple 12.5 sq ft tomato",  
    "apple 12.5 sq fttomato",  
    "apple 12.5sq ft tomato",  
    "apple 12.5sq fttomato",  
    "apple pear12.5 sq ft tomato",  
    "apple pear12.5 sq fttomato",  
    "apple pear12.5sq ft tomato",  
    "apple pear12.5sq fttomato",  
    
    "apple 12.5 sqfts tomato",  
    "apple 12.5 sqftstomato",  
    "apple 12.5sqfts tomato",  
    "apple 12.5sqftstomato",  
    "apple pear12.5 sqfts tomato",  
    "apple pear12.5 sqftstomato",  
    "apple pear12.5sqfts tomato",  
    "apple pear12.5sqftstomato",  
    
    "apple 12.5 sq.fts tomato",  
    "apple 12.5 sq.ftstomato",  
    "apple 12.5sq.fts tomato",  
    "apple 12.5sq.ftstomato",  
    "apple pear12.5 sq.fts tomato",  
    "apple pear12.5 sq.ftstomato",  
    "apple pear12.5sq.fts tomato",  
    "apple pear12.5sq.ftstomato",  
    
    "apple 12.5 sq fts tomato",  
    "apple 12.5 sq ftstomato",  
    "apple 12.5sq fts tomato",  
    "apple 12.5sq ftstomato",  
    "apple pear12.5 sq fts tomato",  
    "apple pear12.5 sq ftstomato",  
    "apple pear12.5sq fts tomato",  
    "apple pear12.5sq ftstomato",  
    
    "apple 12.5 ha tomato",  
    "apple 12.5 hatomato",  
    "apple 12.5ha tomato",  
    "apple 12.5hatomato",  
    "apple pear12.5 hatomato",  
    "apple pear12.5 hatomato",  
    "apple pear12.5hatomato",  
    "apple pear12.5hatomato",  
    
    "apple 12.5 Ha tomato",  
    "apple 12.5 Hatomato",  
    "apple 12.5Ha tomato",  
    "apple 12.5Hatomato",  
    "apple pear12.5 Hatomato",  
    "apple pear12.5 Hatomato",  
    "apple pear12.5Hatomato",  
    "apple pear12.5Hatomato"  
]


for txt in texts:  
    result = extract_size_and_unit(txt)  
    print(f"'{txt}' -> {result}")