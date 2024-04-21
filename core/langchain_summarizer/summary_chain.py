import os
import time
from functools import lru_cache
from core.utils.rate_limiter_easy import rate_limited
from dotenv import load_dotenv
from langchain.chains.llm import LLMChain
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from core.utils.common import text_preview
from core.logging import logger
from core.schema.article_summary import ArticleSummary

# Load the API key from the environment
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("No Gemini API key found. Set the GEMINI_API_KEY environment variable.")

# Prompt template for article summarization
ARTICLE_PROMPT_TEMPLATE = """
Generate the short Summary of this article in 100 words. Keep important information, important points, incident, names and dates in the summary, less filling words, compact and informative. it should return a catching ai_title for the summary. summary which is summary of the article in 100 words, tags related to the article, category of the article, and locations of the article(what locations this article is about)
Strictly use ai_title, summary, tags, category, and locations in the output. Do not use any other words. 

The output should be formatted as a JSON instance that conforms to the JSON schema below.

"ai_title": " a catchy title of the article",
"summary": " a short summary of the article in 100 words",
"tags": ["tag1", "tag2"], # list of up to 5 strings tags
"category": ["category1", "category2"], # list of up to 5 categories that the article belongs to, choose from: [Politics, Economics, Business, Technology, Science, Health, Entertainment, Sports, Education, Environment, Lifestyle, Travel]
"locations": ["location1", "location2"] # list of locations article is talking about, e.g. New York, London, etc.


Here is the Article: 

{article}
"""

@lru_cache(maxsize=32)
def get_llm():
    """
    Get the GoogleGenerativeAI LLM instance with the provided API key.
    """
    return GoogleGenerativeAI(model="gemini-pro", google_api_key=GEMINI_API_KEY)

import time
@rate_limited(1, mode='wait', delay_first_call=False)
def get_summary(article: str, max_retries: int = 3) -> ArticleSummary:
    parser = PydanticOutputParser(pydantic_object=ArticleSummary)
    prompt = PromptTemplate(template=ARTICLE_PROMPT_TEMPLATE, input_variables=["article"])
    llm_chain = LLMChain(llm=get_llm(), prompt=prompt)

    for retry in range(max_retries):
        try:
            response = llm_chain.invoke(input={"article": article})

            if "text" not in response:
                logger.error("Unexpected response format from LLM: %s", response)
                return None
            parsed_summary= parser.parse(response["text"])
            return parsed_summary
        
        except Exception as e:
            logger.error("Error generating summary for article:")
            logger.error(text_preview(article,50))
            logger.exception(e)
            if retry == max_retries - 1:
                logger.error("Maximum retries reached, returning None")
                return None

    # This should never be reached, but just in case
    return None