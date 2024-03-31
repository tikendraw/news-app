import json
from abc import ABC, abstractmethod
from typing import Dict
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from .cache import load_cache, save_cache
from .scrapper_utils import get_random_headers, get_response, get_soup


class BaseScraper(ABC):
    """
    Base class for all scrapers.
    """
    def __init__(self):
        self.cache = load_cache()
        self.headers = [get_random_headers() for _ in range(10)]
        self.articles_data = []

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
        raise NotImplementedError("write_db method not implemented")

    def is_url_cached(self, url):
        return url in self.cache

    def cache_url(self, url):
        self.cache[url] = True

    def save_cache(self):
        save_cache(self.cache)
        
    def write_json(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.articles_data, f, indent=4)  
        print(f"Wrote {len(self.articles_data)} articles to {filename}")

        
    def scrape_links(self, soup: BeautifulSoup, url: str) -> Dict:
        articles = []
        other_pages = []

        for link in soup.find_all('a'):
            relative_url = link.get('href')
            if relative_url:
                absolute_url = urljoin(url, relative_url)

            if absolute_url.endswith('.html'):
                if not self.is_url_cached(absolute_url):
                    articles.append(absolute_url)
                    self.cache_url(absolute_url)
            else:
                if not self.is_url_cached(absolute_url):
                    other_pages.append(absolute_url)
                    self.cache_url(absolute_url)
                    
        return {"articles": articles, "other_pages": other_pages}
    
    @abstractmethod
    def _run():
        raise NotImplementedError("_run method not implemented")
    
    def run(self, *args, **kwargs)->list:
        try:
            self.articles_data = self._run(*args, **kwargs)
        except Exception as e:
            print(f"Error scraping articles: {e}")
            return None

        self.save_cache()
        return self.articles_data