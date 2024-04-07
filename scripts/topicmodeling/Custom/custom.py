import os
import re
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

def preprocess(text, stop_words):
    lemmatizer = WordNetLemmatizer()
    cleaned_text = re.sub('[^A-Za-z]+', ' ', text)
    cleaned_text = re.sub(r'\b\w{1,2}\b', '', cleaned_text)
    tokens = word_tokenize(cleaned_text.lower())
    return " ".join([lemmatizer.lemmatize(w) for w in tokens if w not in stop_words])

def load_and_preprocess_transcripts(directory, stop_words, exclude_files):
    preprocessed_texts = []
    file_names = []
    for filename in os.listdir(directory):
        if filename.endswith('.stm') and filename not in exclude_files:
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                preprocessed_texts.append(preprocess(file.read(), stop_words))
                file_names.append(filename)
    return preprocessed_texts, file_names

def run_topic_modeling(preprocessed_texts, num_clusters):
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(preprocessed_texts)

    km_model = KMeans(n_clusters=num_clusters)
    km_model.fit(tfidf_matrix)

    clusters = km_model.labels_.tolist()
    order_centroids = km_model.cluster_centers_.argsort()[:, ::-1]
    terms = tfidf_vectorizer.get_feature_names_out()

    topics_to_files = {}
    for i in range(num_clusters):
        topic_word = terms[order_centroids[i, 0]]
        topics_to_files[topic_word] = []
    for i, cluster_label in enumerate(clusters):
        topic_word = terms[order_centroids[cluster_label, 0]]
        topics_to_files[topic_word].append(file_names[i])

    return topics_to_files

def select_and_save_topics(topics_to_files, selected_topics_file):
    print("\nIdentified Topics:")
    for topic, filenames in topics_to_files.items():
        print(f"Topic '{topic}':")
        for filename in filenames:
            print(f" - {filename}")
    print("\n")

    selected_topics_input = input("\nEnter the topic names you wish to save, separated by comma (,): ")
    selected_topics = selected_topics_input.split(",")

    # Initialize existing_data as an empty dict
    existing_data = {}
    # Check if the file exists and is not empty before attempting to read it
    if os.path.exists(selected_topics_file) and os.path.getsize(selected_topics_file) > 0:
        try:
            with open(selected_topics_file, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = {}

    for topic in selected_topics:
        topic = topic.strip()
        if topic in topics_to_files:
            if topic in existing_data:
                existing_data[topic].extend(topics_to_files[topic])
            else:
                existing_data[topic] = topics_to_files[topic]

    with open(selected_topics_file, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)

    excluded_files = set()
    for files in existing_data.values():
        excluded_files.update(files)

    return excluded_files

def update_stopwords(stop_words_file):
    new_stopwords = input("Enter any new stopwords to add (separated by commas, or leave blank if none): ")
    if new_stopwords.strip():
        with open(stop_words_file, 'a', encoding='utf-8') as file:
            for stopword in new_stopwords.split(','):
                file.write(f"\n{stopword.strip()}")
        print("Stopwords updated.")

if __name__ == '__main__':
    directory = '../../../data/transcripts/CleanedTranscripts' # Directory of the transcripts to be processed
    selected_topics_file = '../../../data/MappedTopics/selected_topics2.json' # File to store selected topics (clusters) and their corresponding files
    stop_words_file = 'custom_stopwords2.txt' # File to store custom stopwords (appended to nltk's stopwords)

    if not os.path.exists(selected_topics_file): # Create an empty file for selected topics (clusters) if it doesn't exist
        with open(selected_topics_file, 'w') as f:
            json.dump({}, f)

    # Check if custom stopwords file exists; if not, create it from nltk's stopwords
    if not os.path.exists(stop_words_file):
        with open(stop_words_file, 'w', encoding='utf-8') as f:
            for stopword in set(stopwords.words('english')):
                f.write(f"{stopword}\n")
        print(f"Created a new stopwords file with default nltk stopwords at {stop_words_file}")

    with open(stop_words_file, 'r', encoding='utf-8') as file:
        stop_words = set(file.read().splitlines())

    excluded_files = set()
    if os.path.exists(selected_topics_file):
        with open(selected_topics_file, 'r', encoding='utf-8') as f:
            for files in json.load(f).values():
                excluded_files.update(files)

    num_clusters = int(input("Enter the number of topics you wish to generate: "))
    while True:
        preprocessed_texts, file_names = load_and_preprocess_transcripts(directory, stop_words, excluded_files)
        if not preprocessed_texts:
            print("No more transcripts to process.")
            break

        topics_to_files = run_topic_modeling(preprocessed_texts, num_clusters)

        excluded_files.update(select_and_save_topics(topics_to_files, selected_topics_file))

        continue_processing = input("\nDo you want to continue with the remaining transcripts? (yes/no): ").lower()
        if continue_processing != "yes":
            update_stopwords(stop_words_file)
            break

        adjust_num_clusters = input("Do you want to change the number of topics for the next run? (yes/no): ").lower()
        if adjust_num_clusters == "yes":
            try:
                num_clusters = int(input(f"Current number of topics is: {num_clusters}. Enter the new number of topics: "))
            except ValueError:
                print("Invalid number of topics. Keeping the previous number.")

        update_stopwords(stop_words_file)

        with open(stop_words_file, 'r', encoding='utf-8') as file:
            stop_words = set(file.read().splitlines())
