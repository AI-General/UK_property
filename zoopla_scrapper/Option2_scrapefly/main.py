import asyncio
import json
from typing import List

from httpx import AsyncClient, Response
from parsel import Selector

session = AsyncClient(
    headers={
        # use same headers as a popular web browser (Chrome on Windows in this case)
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Language": "en-US,en;q=0.9",
    }
)

def extract_next_data(response: Response) -> dict:
    selector = Selector(text=response.text)
    with open ("response.txt", "w") as f:
        f.write(response, indent=2)
    data = selector.css("script#__NEXT_DATA__::text").get()
    with open("data.txt", "w") as f:
        f.write(data)
    if not data:
        print(f"page {response.url} is not a property listing page")
        return
    data = json.loads(data)
    return data["props"]["pageProps"]


async def scrape_properties(urls: List[str]):
    to_scrape = [session.get(url) for url in urls]
    properties = []
    for response in asyncio.as_completed(to_scrape):
        properties.append(extract_next_data(await response)["listingDetails"])
    return properties

if __name__ == "__main__":
    urls = [
        "https://www.zoopla.co.uk/new-homes/details/68145936"     
    ]
    data = asyncio.run(scrape_properties(urls))
    print (json.dumps(data, indent=2))