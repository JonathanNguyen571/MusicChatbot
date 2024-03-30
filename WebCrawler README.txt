Web Crawler README
Introduction:
The web crawler is a Python script designed to extract relevant URLs and scrape text content from web pages related to song lyrics. 
It uses BeautifulSoup for HTML parsing and requests for HTTP handling.

Features:
Crawls web pages to extract relevant URLs.
Scrapes text content from web pages.
Cleans up text files by removing stop words and punctuation.
Extracts important terms using TF-IDF.
Builds a knowledge base of song lyrics for the chatbot.

Requirements:
Python 3.x
BeautifulSoup
requests
nltk

Usage:
Clone the repository to your local machine.
Ensure directories raw_text and clean_text are in the file path. 
Run the Web_Crawler.py script to start the crawling process.

Appendix:
Sample text files stored in the cleaned_text directory.
Extracted important terms printed to the console.

