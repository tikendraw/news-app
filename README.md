# news-app
Gives you news

## Overview
This application is designed to gather news from various sources, store it, and provide concise summaries. It addresses the problem of information overload by collecting articles from different APIs and web sources and condensing them into easy-to-digest summaries. This allows users to quickly grasp the main points of numerous news articles without needing to read them in full.

## Aim
The primary goal of this project is to create an efficient tool for news consumption. By automatically collecting, storing, and summarizing news, users can stay informed on a wide range of topics without spending excessive time on individual articles. This application seeks to reduce the cognitive burden associated with consuming large quantities of news and make information access more efficient.

## How it Works
News Collection
The application collects news from two main types of sources:

### News APIs: It uses APIs like GNews, Google News API, and NewsData API to fetch articles. These APIs provide structured data in JSON format, which makes it easier to parse and store.

### Web Scraping: For sources not covered by APIs, the application includes a web scraper, such as a CNN scraper, which extracts article content directly from web pages. This involves downloading HTML content, parsing it with BeautifulSoup, and then extracting the relevant parts such as title, author, content, and images.

### Data Storage
A database is used to store the collected articles and their summaries. This allows for persistence and easy retrieval of data. The database is built using SQLAlchemy, which supports SQL operations.

### Summarization
The core of the summarization process is handled by a Language Model. When provided with an article's content, it generates a concise summary along with a title, tags, category, and locations. The model used for summarization in this application is Google's Gemini-pro.

## Problem Solving
This application solves several key problems:

* Information Overload: By providing concise summaries, it reduces the time and effort required to stay informed.

* Data Integration: It combines data from multiple APIs and web sources into a single, manageable system.

* Efficient Access: The stored articles and summaries can be easily accessed for analysis or consumption.

## Basic Usage
Here are some basic things you can do with this application:

* Run the Training Pipeline:
This involves data ingestion, validation, transformation, model training, and evaluation. All training components will be triggered using command python main.py.

* View Summaries in a Basic Frontend:
Run python application.py which will start a webserver using flask. Navigate to http://0.0.0.0:8080/ which will show a basic interface to view some of the summarised articles.

* Access the API:
The API provides operations to manage news articles, you can start it by running python -m uvicorn src.test_db:app --reload --host 0.0.0.0 --port 8000. Navigate to http://0.0.0.0:8000/docs which provides documentation to interact with the rest apis, You can use the API to get news articles, add new ones, or delete and update existing ones.

This application simplifies the process of gathering and consuming news, making information more accessible and manageable.
