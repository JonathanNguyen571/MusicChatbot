# Music Chatbot and Web Crawler
This repository contains two essential components: a Chatbot and a Web Crawler, designed to enhance your experience in exploring and interacting with song lyrics.

## Chatbot README
### Introduction:
The chatbot is a Python script that interacts with users to search for relevant songs based on input lyrics based on the built upon database. It adapts to user preferences over time and provides personalized song recommendations.

### Features:
- Searches for relevant songs based on user input lyrics.
- Saves user preferences (liked/disliked songs) for personalized recommendations.
- Loads and saves user models to maintain state across sessions.

### Requirements:
Python 3.x
scikit-learn
nltk

### Usage:
- Clone the repository to your local machine.
- Ensure the directory user is stored in the file path.
- Run the WebCrawler.py script prior to building the functioning knowledge base.
- Run the MusicBot.py script to start the chatbot.
- Follow the on-screen instructions to interact with the chatbot.

### Appendix:
- Sample user models stored in the users directory.
- Knowledge base loaded from the knowledge_base.pickle file.
- Relevant songs found during user interactions.


## Web Crawler README
### Introduction:
The web crawler is a Python script designed to extract relevant URLs and scrape text content from web pages related to song lyrics. It uses BeautifulSoup for HTML parsing and requests for HTTP handling.

### Features:
- Crawls web pages to extract relevant URLs.
- Scrapes text content from web pages.
- Cleans up text files by removing stop words and punctuation.
- Extracts important terms using TF-IDF.
- Builds a knowledge base of song lyrics for the chatbot.

### Requirements:
Python 3.x
BeautifulSoup
requests
nltk

### Usage:
- Clone the repository to your local machine.
- Ensure directories raw_text and clean_text are in the file path.
- Run the Web_Crawler.py script to start the crawling process.

### Appendix:
- Sample text files stored in the cleaned_text directory.
- Extracted important terms printed to the console.
- Feel free to explore each component and enjoy interacting with song lyrics using our chatbot!

### Disclaimer: Explicit Content
Please be aware that the web crawler component of this project retrieves data from various websites related to song lyrics. While efforts have been made to filter out explicit content, it's essential to understand that the internet is vast and dynamic, and some websites may contain material that some users may find explicit or inappropriate.
