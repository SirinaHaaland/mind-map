import os
import re
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
# Necessary NLTK resources are downloaded automatically
nltk.download('punkt')  # for the word_tokenize function
nltk.download('stopwords')  # for stopwords
nltk.download('wordnet')  # for the WordNet Lemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import numpy as np

def preprocess(text):
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    text = re.sub(r'\b\w{1,2}\b', '', text)
    text = re.sub('[^A-Za-z]+', ' ', text)
    tokens = word_tokenize(text.lower())
    return " ".join([lemmatizer.lemmatize(w) for w in tokens if w not in stop_words])

def load_and_preprocess_transcripts(directory):
    preprocessed_texts = []
    file_names = []
    for filename in os.listdir(directory):
        if filename.endswith('.stm'):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                preprocessed_texts.append(preprocess(file.read()))
                file_names.append(filename)
    return preprocessed_texts, file_names

if __name__ == '__main__':
    directory = '../../../data/transcripts/cleanedtranscripts'
    preprocessed_texts, file_names = load_and_preprocess_transcripts(directory)

    tfidf_vectorizer = TfidfVectorizer(use_idf=True) 
    tfidf_vectorizer.fit_transform(preprocessed_texts) # This is used to calculate the IDF values
    idf_values = tfidf_vectorizer.idf_
    feature_names = tfidf_vectorizer.get_feature_names_out()

    # Create a matrix to hold the IDF values for each document
    idf_only_matrix = np.zeros((len(preprocessed_texts), len(feature_names)))
    for i, text in enumerate(preprocessed_texts):
        tokens = set(text.split())  # Get unique words in the document
        for token in tokens:
            if token in feature_names:
                idx = np.where(feature_names == token)[0][0]
                idf_only_matrix[i][idx] = idf_values[idx]

    num_clusters = 230 # Nr of topics, adjust as needed
    km_model = KMeans(n_clusters=num_clusters)
    km_model.fit(idf_only_matrix)

    clusters = km_model.labels_.tolist()

    order_centroids = km_model.cluster_centers_.argsort()[:, ::-1]
    terms = feature_names

    topics_to_files = {}

    for i in range(num_clusters):
        topic_word = terms[order_centroids[i, 0]]
        topics_to_files[topic_word] = []

    for i, cluster_label in enumerate(clusters):
        topic_word = terms[order_centroids[cluster_label, 0]]
        topics_to_files[topic_word].append(file_names[i])

    with open('idfkmeanstopicmappings.json', 'w', encoding='utf-8') as f:
        json.dump(topics_to_files, f, ensure_ascii=False, indent=4)

    # Print the topics and files for verification
    for topic, filenames in topics_to_files.items():
        print(f"Topic '{topic}':")
        for filename in filenames:
            print(f" - {filename}")
