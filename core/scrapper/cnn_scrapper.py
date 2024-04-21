import asyncio
import random
from typing import Any, Dict, List, Optional, Type
from urllib.parse import urlparse

import aiohttp
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session

from ..logging import logger
from ..schema.article import Article
from .base_scrapper import BaseScraper
from .scrapper_utils import extract_content, extract_image, extract_text

from icecream import ic

class CNNArticle(Article):

    title: Optional[str] = None
    author: Optional[str] = None
    ttr: Optional[str] = None
    published_at: Optional[str] = None
    description: Optional[str] = None
    locations: Optional[list[str]] = None
    content: Optional[str] = None
    images: List[Dict[str, Any]] = []
    source_name:Optional[str] = "CNN"
    url:Optional[str] = None
    meta_data: Optional[Dict[str, Any]] = {}

    def __init__(self, **data):
        if isinstance(data.get("locations"), str):
            data["locations"] = [data["locations"]]

        super().__init__(**data)

        self.meta_data = {'ttr': self.ttr}
        del self.ttr

    def __repr__(self):
        return f"""CNN Scraped Article
        title: {self.title}
        By: {self.author}
        On: {self.published_at}
        Description: {self.description}
        Location: {self.locations}
        Content: {self.content}
        Source URL: {self.url}
        Images: {self.images}
        Source Name: {self.source_name}
        Metadata: {self.meta_data}
        """
    
    
class CNNScraper(BaseScraper):
    
    base_url = "https://edition.cnn.com/"
    
    category_url = {
        "base": "https://edition.cnn.com/",
        'us':"https://edition.cnn.com/us/",
        "world":"https://edition.cnn.com/world/",
        "politics":"https://edition.cnn.com/politics/",
        "business":"https://edition.cnn.com/business/",
        "entertainment":"https://edition.cnn.com/entertainment/",
        "travel":"https://edition.cnn.com/travel/",
        "style":"https://edition.cnn.com/style/",
        "health":"https://edition.cnn.com/health/",
        "sports":"https://edition.cnn.com/sports/",
        
        "africa":"https://edition.cnn.com/world/africa/",
        "asia":"https://edition.cnn.com/world/asia/",
        "americas":"https://edition.cnn.com/world/americas/",
        "australia":"https://edition.cnn.com/world/australia/",
        "china":"https://edition.cnn.com/world/china/",
        "india":"https://edition.cnn.com/world/india/",
        "europe":"https://edition.cnn.com/world/europe/",
        "middle-east":"https://edition.cnn.com/world/middle-east/",
        "united-kingdom":"https://edition.cnn.com/world/united-kingdom/",
        
        "technology":"https://edition.cnn.com/business/tech",
        
        "olympics-2024":"https://edition.cnn.com/sport/paris-olympics-2024",
        "football":"https://edition.cnn.com/sport/football",
        
        "fitness":"https://edition.cnn.com/health/life-but-better/fitness",
        "food":"https://edition.cnn.com/health/life-but-better/food",
        "sleep":"https://edition.cnn.com/health/life-but-better/sleep",
        "mindfulness":"https://edition.cnn.com/health/life-but-better/mindfulness",
        "relationship":"https://edition.cnn.com/health/life-but-better/relationships",
        
        "celebrity":"https://edition.cnn.com/entertainment/celebrities",
        "movies":"https://edition.cnn.com/entertainment/movies",
        "television":"https://edition.cnn.com/entertainment/tv-shows"
        
    }

    selectors =  {
            "title": "body > div.layout__content-wrapper.layout-with-rail__content-wrapper > section.layout__top.layout-with-rail__top > div.headline.headline--has-lowertext > div.headline__wrapper",
            "author": "body > div.layout__content-wrapper.layout-with-rail__content-wrapper > section.layout__top.layout-with-rail__top > div > div.headline__footer > div.headline__sub-container > div > div.byline > div.byline__names",
            "published_at": "body > div.layout__content-wrapper.layout-with-rail__content-wrapper > section.layout__top.layout-with-rail__top > div.headline.headline--has-lowertext > div.headline__footer > div.headline__sub-container > div > div.headline__byline-sub-text > div.timestamp",
            "ttr": "body > div.layout__content-wrapper.layout-with-rail__content-wrapper > section.layout__top.layout-with-rail__top > div.headline.headline--has-lowertext > div.headline__footer > div.headline__sub-container > div > div.headline__byline-sub-text > div.headline__sub-description",
            "description": "body > div.layout__content-wrapper.layout-with-rail__content-wrapper > section.layout__wrapper.layout-with-rail__wrapper > section.layout__main-wrapper.layout-with-rail__main-wrapper > section.layout__main.layout-with-rail__main > article > section > main > div.article__content-container > div.article__content > p.editor-note.inline-placeholder",
            "location":"body > div.layout__content-wrapper.layout-with-rail__content-wrapper > section.layout__wrapper.layout-with-rail__wrapper > section.layout__main-wrapper.layout-with-rail__main-wrapper > section.layout__main.layout-with-rail__main > article > section > main > div.article__content-container > div.article__content > div.source.inline-placeholder > cite > span.source__location",
            "content": "body > div.layout__content-wrapper.layout-with-rail__content-wrapper > section.layout__wrapper.layout-with-rail__wrapper > section.layout__main-wrapper.layout-with-rail__main-wrapper > section.layout__main.layout-with-rail__main > article > section > main > div.article__content-container > div.article__content",
            "images": [
                "body > div.layout__content-wrapper.layout-with-rail__content-wrapper > section.layout__wrapper.layout-with-rail__wrapper > section.layout__main-wrapper.layout-with-rail__main-wrapper > section.layout__main.layout-with-rail__main > article > section > main > div.image__lede.article__lede-wrapper",
                "body > div.layout__content-wrapper.layout-with-rail__content-wrapper > div.image__lede",
                "body > div.layout__content-wrapper.layout-with-rail__conteraw_htmlnt-wrapper > section.layout__wrapper.layout-with-rail__wrapper > section.layout__main-wrapper.layout-with-rail__main-wrapper > section.layout__main.layout-with-rail__main > article > section > main > div.image__lede.article__lede-wrapper > div > div > div.gallery-inline__container > div",
                "body > div.layout__content-wrapper.layout-with-rail__content-wrapper > section.layout__wrapper.layout-with-rail__wrapper > section.layout__main-wrapper.layout-with-rail__main-wrapper > section.layout__main.layout-with-rail__main > article > section > main > div.article__content-container > div.article__content > div.image",
                    ]
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = "https://edition.cnn.com/"
        self.articles_data:list[CNNArticle]=None

    def get_images(self, soup: BeautifulSoup, selector: str) -> List[Dict[str, Optional[str]]]:
        """Extract image URLs, captions, and credits from a BeautifulSoup object."""
        images = []
        for image in soup.select(selector):
            try:
                image_url = extract_content(image, "img[src]", extract_fn=extract_image)
                caption_div = image.find("div", itemprop="caption")
                caption = extract_content(caption_div, "span", extract_fn=extract_text) if caption_div else None
                credit = extract_content(image, "figcaption", extract_fn=extract_text)
                images.append({"image_url": image_url, "caption": caption, "credit": credit})
            except (AttributeError, TypeError) as e:
                logger.error("Error extracting image: {e}", exc_info=True)
        return images
    
    
    def scrape_article(self, soup: BeautifulSoup) -> Dict:
        
        title = extract_content(soup, self.selectors["title"])
        author = extract_content(soup, self.selectors["author"])
        published_at = extract_content(soup, self.selectors["published_at"])
        ttr = extract_content(soup, self.selectors["ttr"])
        description = extract_content(soup, self.selectors["description"])
        location = extract_content(soup, self.selectors["location"])

        content_element = soup.select_one(self.selectors["content"])
        content = ' '.join(p.get_text(strip=True) for p in content_element.find_all('p', attrs={'data-component-name': 'paragraph'})) if content_element else None
        images = []
        
        for image_selector in self.selectors["images"]:
            ii = self.get_images(soup, image_selector)
            images += ii

        return {
            "title": title,
            "author": author,
            "published_at": published_at,
            "ttr": ttr,
            "description": description,
            "location": location,
            "content": content,
            "images": images
        }
        
    def parse_scraped_article(self, article: Dict, *args, **kwargs) -> CNNArticle:
        """Parse a scraped article dictionary into a CNNArticle object."""
        return CNNArticle(
            title=article["title"],
            author=article["author"],
            published_at=article["published_at"],
            ttr=article["ttr"],
            description=article["description"],
            locations = article["location"],
            content=article["content"],
            images=article["images"],
            url=kwargs.get("url"),
            )

    def get_url(self, category:str) -> str:
        if category not in self.category_url:
            raise ValueError(f"Invalid category: {category}. Must be one of {self.category_url.keys()}")
        return self.category_url[category]
    
    def filter_scrapable_urls(self, links: Dict[str, List[str]]) -> List[str]:
        scrapable_links = []
        base_domain = urlparse(self.base_url).netloc
        links = links['articles']
        
        for link in links:
            link_domain = urlparse(link).netloc
            if link_domain == base_domain:
                scrapable_links.append(link)
            else:
                logger.warning(f"(Outside {base_domain} domain) :: Skipping {link}")

        logger.debug(f"Found {len(scrapable_links)} Scrapable article links")
        return scrapable_links    
    
    def _scrape_urls(self, urls: list[str], n = -1) -> list[CNNArticle]:
        urls = self.get_n_links(urls, n)

        articles= asyncio.run(self.fast_scrape_articles(urls))
        return articles
        
    from icecream import ic
    def _run(self, category:str='base', n:int=-1, filter_empty_articles:bool=True)-> list[CNNArticle]:
        url = self.get_url(category=category)
        response = self.get_response(url, headers=random.choice(self.headers))
        soup = self.get_soup(response.text)

        links = self.scrape_links_from_soup(soup=soup, url=self.base_url)
        if not links:
            return []

        links = self.filter_scrapable_urls(links)

        articles= self._scrape_urls(urls=links, n=n)
        
        return self.filter_empty_articles(articles) if filter_empty_articles else articles
                    

    def write_db(self, session:Session, orm_class:Type):
        pass        
        
    async def async_get_html(self, url:str, session:aiohttp.ClientSession) -> str:
        headers = random.choice(self.headers)
        async with session.get(url, headers=headers) as response:
            return await response.text()

    async def async_scrape_pipeline(self, url:str, session:aiohttp.ClientSession) -> CNNArticle:
        html = await self.async_get_html(url, session)
        soup = self.get_soup(html, 'html.parser')
        info= self.scrape_article(soup)
        return self.parse_scraped_article(info, url=url)

    async def fast_scrape_articles(self, urls:list[str]):
        async with aiohttp.ClientSession() as session:
            tasks = [self.async_scrape_pipeline(url, session) for url in urls]
            return await asyncio.gather(*tasks)


    