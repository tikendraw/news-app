import asyncio
import random
from pathlib import Path
from pprint import pprint
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urljoin

import aiohttp
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from pydantic import BaseModel

HEADERS = [
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
    },
    {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
    },
    {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
    },
]


def scrape_links(soup:BeautifulSoup, url:str)->Dict:
    articles = []
    other_pages = []
    for link in soup.find_all('a'):
        relative_url = link.get('href')
        if relative_url:
            absolute_url = urljoin(url, relative_url)

        if absolute_url.endswith('.html') :
            if absolute_url not in articles:
                articles.append(absolute_url)
        else:
            other_pages.append(absolute_url)
    return {"articles": list(articles), "other_pages": list(other_pages)}


def get_response(url:str, headers=None, **kwargs)->requests.Response:
    response = requests.get(url, headers=headers, **kwargs)
    print(f"Response code: {response.status_code}")
    # Raise an exception for non 200 status codes
    response.raise_for_status()
    return response

def get_soup(html:str, parser:str="html.parser", **kwargs)->BeautifulSoup:
    return BeautifulSoup(html, "html.parser", **kwargs)


def get_random_headers():
    ua = UserAgent()
    user_agent = ua.random

    return {
        'User-Agent': user_agent,
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }
