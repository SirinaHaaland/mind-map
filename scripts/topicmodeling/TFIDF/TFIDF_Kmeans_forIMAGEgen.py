"""
Same script as TFIDFwithKmeans.py, but will generate one topic name
pr transcript. This is for generating images for each topic.
"""
import os
import re
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

def preprocess(text):
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
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
    directory = '../../../data/transcripts/CleanedTranscripts'
    preprocessed_texts, file_names = load_and_preprocess_transcripts(directory)

    tfidf_vectorizer = TfidfVectorizer() 
    tfidf_matrix = tfidf_vectorizer.fit_transform(preprocessed_texts) # calculates the TF-IDF scores for all terms in the documents and returns a matrix representing these scores.

    num_clusters = 2329  # number of topics
    km_model = KMeans(n_clusters=num_clusters) # creates a K-Means model with the specified number of clusters
    km_model.fit(tfidf_matrix) # fits the K-Means model to the TF-IDF matrix, performing the clustering process. After fitting, the model assigns each document to one of the num_clusters clusters based on their TF-IDF features

    clusters = km_model.labels_.tolist() # list of cluster labels (assignments) for each document

    # determine the top word for each cluster
    order_centroids = km_model.cluster_centers_.argsort()[:, ::-1] # sorts the cluster centers by their TF-IDF scores in descending order of importance, helps to identify the most representative words for each cluster
    terms = tfidf_vectorizer.get_feature_names_out() # list of terms (words) used in the TF-IDF matrix

    topics_to_files = {}

    for i in range(num_clusters):
        topic_word = terms[order_centroids[i, 0]]  # this loop iterates over each cluster and selects the most significant term (word) for each cluster based on the sorted centroids. It initializes an empty list for each top word in the topics_to_files dictionary, where filenames will be appended.
        topics_to_files[topic_word] = []

    for i, cluster_label in enumerate(clusters): # this loop goes through each document, identifies the top word for its cluster, and appends the document's filename to the corresponding list in the topics_to_files dictionary
        topic_word = terms[order_centroids[cluster_label, 0]]
        topics_to_files[topic_word].append(file_names[i])

    with open('tfidf_kmeans_topics_forIMAGEgen.json', 'w', encoding='utf-8') as f:
        json.dump(topics_to_files, f, ensure_ascii=False, indent=4)

    for topic, filenames in topics_to_files.items():
        print(f"Topic '{topic}':")
        for filename in filenames:
            print(f" - {filename}")