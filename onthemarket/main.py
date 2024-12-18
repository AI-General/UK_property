import json
import re
import ast
import os
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

async def scrape_properties(urls: List[str]) -> List[dict]:
    properties = []
    try:
        """Scrape Rightmove property listings for property data"""
        to_scrape = [client.get(url) for url in urls]
        for response in asyncio.as_completed(to_scrape):
            response = await response
            print(response.text)
    except Exception as e:
        print("Error has occured during scraping properties", e)
    return properties
    
async def run():
    property_data = await scrape_properties(["https://www.onthemarket.com/for-sale/property/london/?bounding-box=s_y_I%7BdfRhdqO%7C%7Cj_A&max-price=230000&min-price=170000&view=map-only"])
    
if __name__ == "__main__":
    asyncio.run(run())