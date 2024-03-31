import json
import os
import urllib.parse
import urllib.request
from typing import Optional

import requests
from icecream import ic
from pydantic import BaseModel, Field, validator

from ...logging import logger
from ..schema import GNewsArticle
from .base_api import NewsAPI

LANGUAGES = ["ar","zh","nl","en","fr","de","el","he","hi","it","ja","ml","mr","no","pt","ro","ru","es","sv","ta","te","uk",
]
COUNTRIES = ["au","br","ca","cn","eg","fr","de","gr","hk","in","ie","il","it","jp","nl","no","pk","pe","ph","pt","ro","ru","sg","es","se","ch","tw","ua","gb","us",
]
CATEGORIES = ["general","world","nation","business","technology","entertainment","sports","science","health",
]

class GNewsAPIError(Exception):
    pass

	    
class GNewsAPI(NewsAPI):
    ERROR_MESSAGES = {
        400: "Bad Request -- Your request is invalid.",
        401: "Unauthorized -- Your API key is wrong.",
        403: "Forbidden -- You have reached your daily quota, the next reset is at 00:00 UTC.",
        429: "Too Many Requests -- You have made more requests per second than you are allowed.",
        500: "Internal Server Error -- We had a problem with our server. Try again later.",
        503: "Service Unavailable -- We're temporarily offline for maintenance. Please try again later.",
    }

    def __init__(self, apikey: str):
        super().__init__()

        self.apikey = apikey
        self.base_url = "https://gnews.io/api/v4/"

        
    @validator("apikey")
    def validate_apikey(cls, v: str) -> str:
        if not v:
            try:
                v = os.environ.get("GNEWS_API_KEY")
            except KeyError as e:
                raise ValueError(
                    "API key is required. Get it from https://gnews.io/ . Pass as argument or set GNEWS_API_KEY environment variable"
                ) from e
        return v


    def _make_request(self, **kwargs: dict) -> dict:
        """
        Construct the API request URL and send a GET request to the
        appropriate endpoint (`"search"` or `"top-headlines"`) based on the
        presence of the `"q"` parameter in the `kwargs`.

        Parameters
        ----------
        **kwargs : dict
            The query parameters for the API request.

        Returns
        -------
        requests.Response
            The response object from the API request.

        Raises
        ------
        GNewsAPIError
            If the API request fails with a known error code.
        """
        params = {k: v for k, v in kwargs.items() if v is not None}
        
        
        if "q" in kwargs:
            endpoint = "search"
            if 'category' in kwargs:
                params.pop('category')
        else:
            endpoint = "top-headlines"
            
        logger.debug("Making request to %s with params %s", endpoint, params)
        url = f"{self.base_url}{endpoint}?apikey={self.apikey}"

        params = urllib.parse.urlencode(params)
        url = f"{url}&{params}" if params else url

        try:
            with urllib.request.urlopen(url) as response:
                if response.status != 200:
                    raise GNewsAPIError(self.ERROR_MESSAGES.get(response.status, f"Unexpected error: {response.reason}"))
                logger.debug("Response code: %s", response.status)
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            raise GNewsAPIError(self.ERROR_MESSAGES.get(e.code, f"Unexpected error: {e.reason}")) from e
        except (urllib.error.URLError, json.JSONDecodeError) as e:
            raise GNewsAPIError(f"Failed to make request: {e}") from e

    def parse_news(self, news_dict: dict, **kwargs) -> Optional[list[GNewsArticle]]:
        """
        Parse the response dictionary from the API and convert it to a list
        of `GNewsArticle` instances.

        Parameters[]
        ----------
        news_dict : dict
            The response dictionary from the API.
        **kwargs : dict
            Additional keyword arguments to pass to the `GNewsArticle`
            instances.

        Returns
        -------
        Optional[list[GNewsArticle]]
            A list of `GNewsArticle` instances, or `None` if no articles are
            found.
        """
        # ic(news_dict)
        articles = news_dict.get("articles", [])
        if not articles:
            return None
        
        parsed_articles = []
        for article in articles:
            category = kwargs.get('category', None)
            country =  kwargs.get('country', None)
            language = kwargs.get('lang', None)
            metadata = {
                'query': kwargs.get('q', '')
            } if 'q' in kwargs else {}
            
            if category:
                article['category'] = [category]
            if country:
                article['locations'] = [country]
            if language:
                article['language'] = [language]
            if metadata:
                article['metadata'] = metadata
            
            parsed_articles.append(
                GNewsArticle(**article)
            )
            
        return parsed_articles


    def get_news(self, **kwargs: dict) -> Optional[list[GNewsArticle]]:
        """
        Get news articles based on the provided query parameters.

        Parameters
        ----------
        **kwargs : dict
            The query parameters for the API request. Possible keyword
            arguments are:

            - `q` (optional): The search query for the `"search"` endpoint.
            - `category` (optional): The category for the news articles.
            - `lang` (optional): The language code for the news articles.
            - `country` (optional): The country code for the news articles.
            - `max` (optional): The maximum number of news articles to retrieve.
            - `in` (optional): The attributes to search for the keywords in.
            - `nullable` (optional): The attributes that can have `null` values.
            - `from` (optional): The publication date to filter articles from.
            - `to` (optional): The publication date to filter articles up to.
            - `sortby` (optional): The sorting method for the search results.
            - `page` (optional): The page number for pagination.
            - `expand` (optional): Whether to include the full content of the articles.

        Returns
        -------
        Optional[list[GNewsArticle]]
            A list of `GNewsArticle` instances, or `None` if there's an error
            retrieving the news articles.

        Raises
        ------
        GNewsAPIError
            If there's an error retrieving the news articles.
        """
        response = self._make_request(**kwargs)
        return self.parse_news(response, **kwargs)
    


