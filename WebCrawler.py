from urllib.parse import urlparse, unquote
import requests
import pickle
from bs4 import BeautifulSoup
import os
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer


# Function to crawl URLs and extract relevant URLs
def crawl_urls(initial_urls, num_urls):
    crawled_urls = set(initial_urls)
    relevant_urls = set()

    while len(relevant_urls) < num_urls:
        url = crawled_urls.pop()
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract links from the page
            links = soup.find_all('a', href=True)
            for link in links:
                new_url = link['href']
                if new_url.startswith('http') and new_url not in crawled_urls:
                    crawled_urls.add(new_url)
                    relevant_urls.add(new_url)

                    if len(relevant_urls) >= num_urls:
                        break
        except Exception as e:
            print(f"Error crawling URL: {url}, {e}")

    return relevant_urls


def get_song_name(url):
    # Parse the URL
    parsed_url = urlparse(url)

    # Extract the path component of the URL
    path_components = parsed_url.path.split('/')

    # Look for keywords that might indicate the song name
    keywords = ['lyrics', 'song', 'track']

    # Iterate through the path components to find the song name
    for component in reversed(path_components):
        if isinstance(component, bytes):  # Check if the component is bytes
            component = component.decode('utf-8')  # Decode bytes to string using UTF-8

        # Decode URL-encoded components
        decoded_component = unquote(component)

        # Check if the component contains any keywords
        if any(keyword in decoded_component.lower() for keyword in keywords):
            # Remove file extensions or query parameters
            song_name = decoded_component.split('.')[0].split('?')[0]

            # Return the extracted song name
            return song_name.strip()  # Strip leading/trailing spaces

    # If no keywords are found, return a default name or None
    return 'unknown_song'


# Function to scrape text from each URL and save it to separate files
def scrape_text(urls, output_dir):
    for idx, url in enumerate(urls):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            text = soup.get_text()

            song_name = get_song_name(url)

            # Write text to a separate file with explicit encoding
            with open(os.path.join(output_dir, f"{song_name}.txt"), 'w', encoding='utf-8') as file:
                file.write(text)
        except Exception as e:
            print(f"Error scraping URL: {url}, {e}")


# Function to clean up text files
def clean_text_files(input_dir, output_dir):
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    translator = str.maketrans('', '', string.punctuation)

    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            try:
                with open(os.path.join(input_dir, filename), 'r', encoding='utf-8') as file:
                    text = file.read().lower()
                    words = word_tokenize(text)
                    words = [word.translate(translator) for word in words if word.isalnum()]
                    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]

                    cleaned_text = ' '.join(words)

                    with open(os.path.join(output_dir, filename), 'w', encoding='utf-8') as cleaned_file:
                        cleaned_file.write(cleaned_text)
            except Exception as e:
                print(f"Error cleaning file: {filename}, {e}")


# Function to extract important terms using TF-IDF
def extract_important_terms(input_dir, num_terms):
    corpus = []
    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            with open(os.path.join(input_dir, filename), 'r', encoding='utf-8') as file:
                corpus.append(file.read())

    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)

    feature_names = tfidf_vectorizer.get_feature_names_out()
    scores = tfidf_matrix.sum(axis=0).A1

    # Get top important terms
    top_terms_indices = scores.argsort()[-num_terms:][::-1]
    top_terms = [feature_names[i] for i in top_terms_indices]

    return top_terms


# Function to build a knowledge base
def build_knowledge_base(input_dir, important_terms):
    knowledge_base = {}

    for term in important_terms:
        facts = []
        for filename in os.listdir(input_dir):
            if filename.endswith(".txt"):
                with open(os.path.join(input_dir, filename), 'r', encoding='utf-8') as file:
                    text = file.read()
                    if term in text:
                        # Store the name of the text file along with its content
                        facts.append((filename, text))

        knowledge_base[term] = facts

    return knowledge_base


def store_crawled_urls(urls, output_file):
    try:
        with open(output_file, 'w') as f:
            for url in urls:
                f.write(url + '\n')
        print(f"Crawled URLs successfully stored in {output_file}")
    except Exception as e:
        print(f"Error storing crawled URLs: {str(e)}")


# Main function
if __name__ == "__main__":
    # Initial URLs related to song lyrics
    initial_urls = [
        'https://www.lyrics.com/',
        'https://genius.com/',
        'https://www.azlyrics.com/'
    ]

    # Number of relevant URLs to crawl
    num_urls = 60

    # Output directories
    raw_text_dir = 'raw_text'
    cleaned_text_dir = 'cleaned_text'

    # Crawl relevant URLs
    relevant_urls = crawl_urls(initial_urls, num_urls)

    # Scrape text from each URL and save it to separate files
    scrape_text(relevant_urls, raw_text_dir)

    # Clean up text files
    clean_text_files(raw_text_dir, cleaned_text_dir)

    # Extract important terms
    important_terms = extract_important_terms(cleaned_text_dir, 25)

    print("Top 25 important terms:")
    for term in important_terms:
        print(term)

    store_crawled_urls(relevant_urls, 'crawled_urls.txt')

    # Build searchable knowledge base
    knowledge_base = build_knowledge_base(cleaned_text_dir, important_terms)

    # Store knowledge base in a pickle database
    with open('knowledge_base.pickle', 'wb') as f:
        pickle.dump(knowledge_base, f)
