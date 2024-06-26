from functools import partial
from typing import Callable, Dict, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from .scrapper_cache import cache_url, is_url_cached, load_cache, save_cache

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


def get_response(url:str,  **kwargs_for_requests_get)->requests.Response:
    response = requests.get(url, **kwargs_for_requests_get)
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

def extract_text(element: Optional[BeautifulSoup]) -> Optional[str]:
    """Extract text content from a BeautifulSoup element."""
    return element.get_text().strip() if element else None

def extract_attr(element: Optional[BeautifulSoup], attr: str) -> Optional[str]:
    """Extract an attribute value from a BeautifulSoup element."""
    return element.get(attr) if element else None

def extract_content(soup: BeautifulSoup, selector: str, extract_fn: Callable[[BeautifulSoup], Optional[str]] = extract_text) -> Optional[str]:
    """Extract content from a BeautifulSoup element using a selector and an extraction function."""
    element = soup.select_one(selector)
    return extract_fn(element) if element else None

def extract_image(element: BeautifulSoup) -> Optional[str]:
    """Extract image URL from a BeautifulSoup element."""
    extract_img = partial(extract_attr, attr="src")
    return extract_img(element)