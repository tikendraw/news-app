from abc import ABC, abstractmethod
from functools import partial
from typing import Callable, Dict, List, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from .scrapper_utils import scrape_links, get_response, get_soup


class BaseScraper(ABC):


    @abstractmethod
    def scrape_article(self, soup: BeautifulSoup) -> Dict:
        """
        Extract article data from a given HTML page.
        """
        pass

    @abstractmethod
    def parse_scraped_article(self, article: Dict, *args, **kwargs) :
        """
        Parse the scraped article data into a more useful format pydantic model.
        """
        pass
    
    def get_response(self, url: str, **kwargs) -> requests.Response:
        """Get a response from a given URL."""
        return get_response(url, **kwargs)
        
    
    def get_soup(self, html: str, parser: str="html.parser", **kwargs) -> BeautifulSoup:
        """Parse HTML content into a BeautifulSoup object."""
        return get_soup(html, parser, **kwargs)
    
    @abstractmethod
    def write_db():
        raise NotImplementedError
    
    def scrape_links(self, soup:BeautifulSoup, url:str) -> Dict:
        return scrape_links(soup, url)