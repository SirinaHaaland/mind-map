import os
import re
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

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

def select_and_save_topics(topics_to_files):
    print("\nIdentified Topics:")
    for topic, filenames in topics_to_files.items():
        print(f"Topic '{topic}':")
        for filename in filenames:  # Show all filenames for thorough review
            print(f" - {filename}")
        print("\nIdentified Topics:")
    for topic in topics_to_files:
        print(f"Topic '{topic}': {len(topics_to_files[topic])} files")
            
    selected_topics_input = input("\nEnter the topic names you wish to save, separated by comma (,): ")
    selected_topics = selected_topics_input.split(",")

    selected_topics_dict = {topic.strip(): topics_to_files[topic.strip()] for topic in selected_topics if topic.strip() in topics_to_files}

    excluded_files = set()
    for topic, files in selected_topics_dict.items():
        excluded_files.update(files)

    with open('selected_topics.json', 'a', encoding='utf-8') as f:
        json.dump(selected_topics_dict, f, ensure_ascii=False, indent=4)

    return excluded_files

def update_stopwords(stop_words_file):
    new_stopwords = input("Enter any new stopwords to add (separated by commas, or leave blank if none): ")
    if new_stopwords.strip():  # Check if the input is not empty
        with open(stop_words_file, 'a', encoding='utf-8') as file:
            # Add each new stopword on a new line
            for stopword in new_stopwords.split(','):
                file.write(f"\n{stopword.strip()}")
        print("Stopwords updated.")

if __name__ == '__main__':
    directory = '../../../data/transcripts/CleanedTranscripts'
    stop_words_file = 'custom_stopwords.txt'  # Updated to use the variable for consistency
    with open(stop_words_file, 'r', encoding='utf-8') as file:
        stop_words = set(file.read().splitlines())

    excluded_files = set()
    num_clusters = 180  # Initial number of topics
    while True:
        preprocessed_texts, file_names = load_and_preprocess_transcripts(directory, stop_words, excluded_files)
        if not preprocessed_texts:
            print("No more transcripts to process.")
            break

        topics_to_files = run_topic_modeling(preprocessed_texts, num_clusters)

        excluded_files.update(select_and_save_topics(topics_to_files))

        continue_processing = input("\nDo you want to continue with the remaining transcripts? (yes/no): ").lower()
        if continue_processing != "yes":
            break

        adjust_num_clusters = input("Do you want to change the number of topics for the next run? (yes/no): ").lower()
        if adjust_num_clusters == "yes":
            try:
                num_clusters = int(input(f"Number of topics now is: {num_clusters}. Enter the new number of topics: "))
            except ValueError:
                print("Invalid number of topics. Keeping the previous number.")
        
        # New part: Prompt for updating stopwords
        update_stopwords(stop_words_file)
        
        # Reload stopwords in case they were updated
        with open(stop_words_file, 'r', encoding='utf-8') as file:
            stop_words = set(file.read().splitlines())
