import json
from abc import ABC, abstractmethod
from typing import Dict
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from ..logging import logger
from ..schema.article import Article
from .scrapper_cache import load_cache, save_cache
from .scrapper_utils import get_random_headers, get_response, get_soup


class BaseScraper(ABC):
    """
    Base class for all scrapers.
    """
    def __init__(self, enable_cache: bool = True) -> None:
        self.enable_cache = enable_cache
        
        if self.enable_cache:
            self.cache = load_cache()
        
        self.headers = [get_random_headers() for _ in range(10)]
        self.articles_data = []

    @abstractmethod
    def scrape_article(self, soup: BeautifulSoup) -> Dict:
        """False
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
        return url in self.cache if self.enable_cache else False

    def cache_url(self, url):
        self.cache[url] = True

    def save_cache(self):
        save_cache(self.cache)
        
    def write_json(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.articles_data, f, indent=4)  
        print(f"Wrote {len(self.articles_data)} articles to {filename}")
    
    def scrape_links_from_soup(self, soup: BeautifulSoup, url: str) -> Dict:
        articles = set()
        other_pages = set()

        for link in soup.find_all('a'):
            relative_url = link.get('href')
            if not relative_url:
                continue

            absolute_url = urljoin(url, relative_url)
            is_article = absolute_url.endswith('.html')

            if is_article:
                if not self.is_url_cached(absolute_url):
                    articles.add(absolute_url)
            else:
                other_pages.add(absolute_url)

        logger.debug(f"Found {len(articles)} articles and {len(other_pages)} other pages")
        return {"articles": list(articles), "other_pages": list(other_pages)}


    def __cache_and_return_articles(self,cache:bool = None, articles:list[Article]=None) -> list[Article]:
        if cache is None:
            cache = self.enable_cache

        if cache:
            for article in articles:
                self.cache_url(article.url)

            self.save_cache()

        return articles

    
    @abstractmethod
    def _scrape_urls(self, *args, **kwargs) -> list[Article]:
        raise NotImplementedError("_scrape_urls method not implemented")
    
    def scrape_urls(self, cache:bool=None, *args, **kwargs) -> list[str]:
        try:
            self.articles_data = self._scrape_urls(*args, **kwargs)
        except Exception as e:
            raise e
        
        return self.__cache_and_return_articles(cache=cache, articles=self.articles_data)

    
    @abstractmethod
    def _run(self, *args, **kwargs) -> list[Article]:
        raise NotImplementedError("_run method not implemented")
    
    def run(self, cache:bool=None, *args, **kwargs )->list:
        try:
            self.articles_data = self._run(*args, **kwargs)
        except Exception as e:
            raise e
        
        return self.__cache_and_return_articles(cache=cache, articles=self.articles_data)
    
    
    def get_n_links(self, links:list[str], n:int)->list[str]:
        if n==-1 or n>=len(links):
            return links
        elif n>0 and n<len(links):
            return links[:n]


    def filter_empty_articles(self, articles: list[Article]) -> list[Article]:
        full_articles=[]
            
        for article in articles:
            if article.content is not None:
                full_articles.append(article)
                
        logger.debug(f"Found {len(full_articles)} full articles")
        logger.debug(f"Filtered {len(articles)-len(full_articles)} empty articles")
        return full_articles
