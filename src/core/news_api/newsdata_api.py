import json
import os
import urllib.parse
import urllib.request
from typing import Dict, List, Optional

from icecream import ic
from newsdataapi import NewsDataApiClient
from pydantic import BaseModel, Field, root_validator, validator

from ..news_model import NewsDataArticle
from .base_api import NewsAPI

# COUNTRIES = [
# "af", "al", "dz", "ao", "ar", "au", "at", "az", "bs", "bh",
# "bd", "bb", "by", "be", "bz", "bm", "bt", "bo", "ba", "bw",
# "br", "bn", "bg", "kh", "cm", "ca", "cv", "ky", "cf", "cl",
# "cn", "co", "km", "cg", "cr", "hr", "cu", "cy", "cz", "cd",
# "dk", "dj", "dm", "do", "ec", "eg", "sv", "ee", "et", "fj",
# "fi", "fr", "pf", "ga", "ge", "de", "gh", "gr", "gt", "gn",
# "ht", "hn", "hk", "hu", "is", "in", "id", "ir", "iq", "ie",
# "il", "it", "ci", "jm", "jp", "jo", "kz", "ke", "kw", "kg",
# "la", "lv", "lb", "ly", "lt", "lu", "mk", "mg", "mw", "my",
# "mv", "ml", "mt", "mh", "mr", "mu", "mx", "md", "mc", "mn",
# "me", "ma", "mz", "mm", "na", "np", "nl", "nz", "ne", "ng",
# "kp", "no", "om", "pk", "pa", "pg", "py", "pe", "ph", "pl",
# "pt", "pr", "qa", "ro", "ru", "rw", "ws", "sa", "sn", "rs",
# "sg", "sk", "si", "sb", "so", "za", "kr", "es", "lk", "sd",
# "se", "ch", "sy", "tw", "tj", "tz", "th", "to", "tn", "tr",
# "tm", "ug", "ua", "ae", "gb", "us", "uy", "uz", "vu", "ve",
# "vn", "ye", "zm", "zw"
# ]


class NewsDataAPIError(Exception):
    pass


class NewsDataAPI(NewsAPI, NewsDataApiClient):
    BASE_URL = "https://newsdata.io/api/1/news"
    ERROR_MESSAGES = {
        400: "Parameter missing or malformed.",
        401: "Unauthorized. API key is invalid or missing.",
        403: "CORS policy failed. IP/Domain restricted.",
        409: "Parameter duplicate.",
        415: "Unsupported type.",
        422: "Unprocessable entity.",
        429: "Too many requests.",
        500: "Internal server error.",
    }

    def __init__(self, apikey: str):
        self.apikey = apikey

        if not self.apikey:
            try:
                apikey = os.environ.get("NEWSDATA_API_KEY")
            except KeyError as e:
                raise ValueError(
                    "API key is required. Get if from https://newsdata.io/register . pass as argument or set NEWSDATA_API_KEY environment variable"
                ) from e

        self.api = NewsDataApiClient(apikey=self.apikey)

    def _make_request(self, **kwargs) -> Dict:
        response = self.api.news_api(**kwargs)
        if response["status"] != "success":
            try:
                error_code = int(response.get("code", 0))
                ic(error_code)
            except ValueError:
                error_code = 0

            error_msg = self.ERROR_MESSAGES.get(error_code, "Unknown error")
            raise Exception(f"Error {error_code}: {error_msg}")
        return response

    def parse_news(self, data: Dict) -> Optional[List[NewsDataArticle]]:
        articles = data.get("results", [])

        if articles:
            # ic(articles)
            return [NewsDataArticle(**article_data) for article_data in articles]
        else:
            print("No aricles found")
            return None

    def get_news(self, **kwargs) -> Optional[List[NewsDataArticle]]:
        try:
            response_data = self._make_request(**kwargs)
            return self.parse_news(response_data)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None
