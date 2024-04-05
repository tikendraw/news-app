import os
from typing import List

from dotenv import load_dotenv
from langchain.chains.llm import LLMChain
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field, validator

#Import Modules
from langchain_google_genai import GoogleGenerativeAI
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

# Here's another example, but with a compound typed field.
class ArticleSummary(BaseModel):
    ai_title: str = Field(description="Catching title for an article")
    content_summary: str = Field(description="Summary of an article in 100 words only")
    tags: List[str] | None = Field(description="tags related to the article")
    category: list[str] | None = Field(description="Category of an article")
    locations: list[str] | None = Field(description="Location this article is about")
    


article_prompt_template = """Generate the short Summary of this article in 100 words. 
Keep important information, important points, incident, names and dates in the summary, less filling words, compact and informative. it should return a catching ai_title for the summary.
content_summary which is summary of the article in 100 words, tags releated to the article, category of the article, and 
location of the article(what location this article is about)

The output should be formatted as a JSON instance that conforms to the JSON schema below.

    "ai_title": " a catchy title of the article",
    "content_summary": " a short summary of the article in 100 words",
    "tags": ["tag1", "tag2"], # list of upto 5 strings tags 
    "category": [category1", "category2], # list of upto 5 categories that the article belongs to , e.g. politics, sports, etc.
    "locations": [location1", "location2], # list of locations article is talking about, e.g. New York, London, etc.


Here is the Article:
{article}
"""

def get_llm():
    import os
    api_key = os.environ.get('GEMINI_API_KEY')
    
    if not api_key:
        raise ValueError("No gemini api key found . set ENVIRONMENT variable 'GEMINI_API_KEY'")
    
    return GoogleGenerativeAI(model="gemini-pro", google_api_key=api_key)

def get_summary(article:str, n:int=3) -> ArticleSummary:
    parser = PydanticOutputParser(pydantic_object=ArticleSummary)
    

    prompt = PromptTemplate(
        template=article_prompt_template,
        input_variables=["article"],
    )


    llm_chain = LLMChain(llm=get_llm(), prompt=prompt)

    try_n = 0
    if try_n<n:
        try:        
            response=llm_chain.invoke(input={"article":article})
            summary = parser.parse(response['text'])
            
            if summary.__class__==ArticleSummary:
                return summary
            else:
                pass
            
        except Exception as e:
            print(e)
        
        try_n += 1
        
    print("Maximum tries reached!!!")
    return None

