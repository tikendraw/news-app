from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


class BaseScraper(ABC):
    def __init__(self, base_url: str, headers: Optional[Dict[str, str]] = None):
        self.base_url = base_url


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
    
    def extract_text(self, element: Optional[BeautifulSoup]) -> Optional[str]:
        """Extract text content from a BeautifulSoup element."""
        return element.get_text(strip=True) if element else None

    def extract_attr(self, element: Optional[BeautifulSoup], attr: str) -> Optional[str]:
        """Extract an attribute value from a BeautifulSoup element."""
        return element.get(attr) if element else None

    def extract_content(self, soup: BeautifulSoup, selector: str, extract_fn: Callable[[BeautifulSoup], Optional[str]] = extract_text) -> Optional[str]:
        """Extract content from a BeautifulSoup element using a selector and an extraction function."""
        element = soup.select_one(selector)
        return extract_fn(element) if element else None

    def extract_image(self, element: BeautifulSoup) -> Optional[str]:
        """Extract image URL from a BeautifulSoup element."""
        extract_img = partial(self.extract_attr, attr="src")
        return extract_img(element)

    def get_response(self, url: str, **kwargs) -> requests.Response:
        """Get a response from a given URL."""
        response = requests.get(url, **kwargs)
        print(f"Response code: {response.status_code}")
        response.raise_for_status()
        return response

        
    
    def get_soup(self, html: str, parser: str="html.parser", **kwargs) -> BeautifulSoup:
        """Parse HTML content into a BeautifulSoup object."""
        return BeautifulSoup(html, parser, **kwargs)
    