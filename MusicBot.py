import random
import pickle
import os
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Load knowledge base from pickle database
with open('knowledge_base.pickle', 'rb') as f:
    knowledge_base = pickle.load(f)


# Load user model
def load_user_model(username, user_dir):
    try:
        with open(os.path.join(user_dir, f'user_{username}_model.txt'), 'r', encoding='utf-8') as file:
            user_model = eval(file.read())  # Convert the string to a dictionary
        return user_model
    except FileNotFoundError:
        return {'likes': [], 'dislikes': []}


# Save user model
def save_user_model(username, user_model, user_dir):
    with open(os.path.join(user_dir, f'user_{username}_model.txt'), 'w', encoding='utf-8') as file:
        file.write(str(user_model))


# Function to preprocess text
def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    translator = str.maketrans('', '', string.punctuation)

    words = word_tokenize(text.lower())
    words = [word.translate(translator) for word in words if word.isalnum()]
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]

    return ' '.join(words)


def search_for_songs(lyrics, knowledge_base):
    relevant_songs = []
    tfidf_vectorizer = TfidfVectorizer()

    # Preprocess user input
    preprocessed_lyrics = preprocess_text(lyrics)

    # Create a list of all songs in the knowledge base along with their names
    all_songs_with_names = [(song[0], song[1]) for songs_list in knowledge_base.values() for song in songs_list]

    # Separate song names and contents
    all_song_names, all_song_contents = zip(*all_songs_with_names)

    # Combine user input with all songs for TF-IDF vectorization
    all_texts = [preprocessed_lyrics] + list(all_song_contents)

    # Transform texts into TF-IDF matrix
    tfidf_matrix = tfidf_vectorizer.fit_transform(all_texts)

    # Calculate cosine similarity between user input and all songs
    similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    # Get the index of the most similar song
    most_similar_index = similarities[1:].argmax()  # Exclude the first element which is the user input

    # Retrieve the most similar song
    if most_similar_index >= 0:
        relevant_song_name = all_song_names[most_similar_index + 1]
        relevant_songs.append(relevant_song_name)

    return relevant_songs


def user_exists(username, user_dir):
    # Construct the file path for the user's text file
    user_file_path = os.path.join(user_dir, f"user_{username}_model.txt")

    # Check if the file exists
    return os.path.isfile(user_file_path)


def retrieve_user_preferences(username, user_dir):
    with open(os.path.join(user_dir, f'user_{username}_model.txt'), 'r', encoding='utf-8') as file:
        content = file.read()
        return content


# Chatbot to talk to the user
def chatbot(user_dir):
    # Get the username from the user
    username = input("You: ")
    lower_case = username.lower()

    # Check if the user's text file exists
    if user_exists(lower_case, user_dir):
        print(f"Welcome back, {username}!")
    else:
        print(f"Hello, {username}!")

    # Load or create user model
    user_model = load_user_model(lower_case, user_dir)

    print("Please type in the lyrics you want to search for.")
    print("Type 'exit' to quit and save the user info. Type 'info' to retrieve user info.")

    while True:
        user_input = input("You: ").lower()

        # Check if the user wants to exit
        if user_input == 'exit':
            # Update the user model with the retrieved song
            save_user_model(lower_case, user_model, user_dir)
            break

        if user_input == 'info':
            print(retrieve_user_preferences(lower_case, user_dir))
            continue

        # Search for relevant songs based on user input
        relevant_song = search_for_songs(user_input, knowledge_base)

        if relevant_song:
            print(f"The song found is {relevant_song}. \nDo you like this song?")

            user_response = input("You: ").lower()
            if user_response == 'yes':
                user_model['likes'].append(relevant_song)
            elif user_response == 'no':
                user_model['dislikes'].append(relevant_song)
            else:
                print("Invalid response. Please type 'yes' or 'no'.")

        else:
            print("Song not found in the database! Please type in different lyrics.")

        # Update the user model with the retrieved song
        save_user_model(lower_case, user_model, user_dir)
        print("Type in lyrics to find another song!")


if __name__ == "__main__":
    greetings = [
        "Hello!",
        "Hi there!",
        "Hey! Welcome to the chatbot.",
        "Greetings!",
        "Hello there!"
    ]

    farewells = [
        "Goodbye!",
        "Farewell!",
        "Until next time!",
        "Take care!",
        "Have a great day!",
        "See you later!",
        "Adios!",
        "Bye for now!",
        "So long!",
        "Bye-bye!",
    ]

    print(random.choice(greetings) + " Type in your name to start!")
    try:
        chatbot("users")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    print(random.choice(farewells))
