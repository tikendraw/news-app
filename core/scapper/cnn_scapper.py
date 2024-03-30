from typing import Dict, List, Optional, Type
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from pydantic import BaseModel
from .scapper_utils import get_random_headers

class CNNArticle(BaseModel):

    title: Optional[str] = None
    author: Optional[str] = None
    published_at: Optional[str] = None
    ttr: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    content: Optional[str] = None
    images: List[Dict[str, Any]] = []
    source_url:Optional[str] = None

    def __repr__(self):
        return f"""CNN Scraped Article
        title: {self.title}
        By: {self.author}
        On: {self.published_at}
        TTR: {self.ttr}
        Description: {self.description}
        Location: {self.location}
        Content: {self.content}
        Source URL: {self.source_url}
        Images: {self.images}
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
                "body > div.layout__content-wrapper.layout-with-rail__conteraw_htmlnt-wrapper > section.layout__wrapper.layout-with-rail__wrapper > section.layout__main-wrapper.layout-with-rail__main-wrapper > section.layout__main.layout-with-rail__main > article > section > main > div.image__lede.article__lede-wrapper > div > div > div.gallery-inline__container > div",
                "body > div.layout__content-wrapper.layout-with-rail__content-wrapper > section.layout__wrapper.layout-with-rail__wrapper > section.layout__main-wrapper.layout-with-rail__main-wrapper > section.layout__main.layout-with-rail__main > article > section > main > div.article__content-container > div.article__content > div.image",
                    ]
        }

    def __init__(self):
        super().__init__(base_url)
        self.headers = [get_random_headers() for _ in range(10)]
        self.articles_data:list[CNNArticle]=None

    

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
            ii = get_images(soup, image_selector)
            images += ii

        return {
            "title": title,
            "author": author,
            "published_at": published_at,
            "ttr": ttr,
            "description": description,
            "location": location,
            "content": content,
            "images": images,
        }
        

    def get_images(self, soup: BeautifulSoup, selector: str) -> List[Dict[str, Optional[str]]]:
        """Extract image URLs, captions, and credits from a BeautifulSoup object."""
        images = []
        for image in soup.select(selector):
            try:
                image_url = extract_content(image, "img[src]", extract_image)
                caption_div = image.find("div", itemprop="caption")
                caption = extract_content(caption_div, "span", extract_text) if caption_div else None
                credit = extract_content(image, "figcaption", extract_text)
                images.append({"image_url": image_url, "caption": caption, "credit": credit})
            except (AttributeError, TypeError) as e:
                print(f"Error extracting image: {e}")
        return images    
    
    def parse_scraped_article(self, article: Dict, *args, **kwargs) -> CNNArticle:
        """Parse a scraped article dictionary into a CNNArticle object."""
        return CNNArticle(
            title=article["title"],
            author=article["author"],
            published_at=article["published_at"],
            ttr=article["ttr"],
            description=article["description"],
            location = article["location"],
            content=article["content"],
            images=article["images"],
            source_url=kwargs.get("source_url"),
            )


    def run(self, category: str='base'):
        
        if category not in self.category_url:
            raise ValueError(f"Invalid category: {category}. Must be one of {self.category_url.keys()}")
        
        url = self.category_url[category]
        
        response = self.get_response(url, headers=random.choice(self.headers))
        soup = self.get_soup(response.text)
        links = self.scrape_links(soup)
        article_links = links["articles"]
        self.articles_data = asyncio.run(self.fast_scrape_articles(article_links))
        
    
    def write_json(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.articles_data, f, indent=4)  
        print(f"Wrote {len(self.articles_data)} articles to {filename}")
        
    
    def write_csv(self, filename):
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(self.articles_data[0].keys())
            for article in self.articles_data:
                writer.writerow(article.values())
        print(f"Wrote {len(self.articles_data)} articles to {filename}")
        

    def write_db(self, session:Session, orm_class:Type):
        for article in self.articles_data:
            article_orm = orm_class(**article.dict())
            session.add(article_orm)
        session.commit()
        session.close()
        print(f"Wrote {len(self.articles_data)} articles to database")
        
        

    async def async_get_html(self, url:str, session:aiohttp.ClientSession) -> str:
        headers = random.choice(self.headers)
        async with session.get(url, headers=headers) as response:
            return await response.text()

    async def async_scrape_pipeline(self, url:str, session:aiohttp.ClientSession) -> CNNArticle:
        html = await async_get_html(url, session)
        soup = self.get_soup(html, 'html.parser')
        info= scrape_article(soup)
        return parse_scraped_article(info, source_url=url)

    async def fast_scrape_articles(self, urls:list[str]):
        async with aiohttp.ClientSession() as session:
            tasks = [async_scrape_pipeline(url, session) for url in urls]
            return await asyncio.gather(*tasks)
