"""TF-IDF combines two metrics: Term Frequency (TF) and Inverse 
Document Frequency (IDF). TF measures how frequently a term occurs
in a document, while IDF measures how important a term is within 
the entire corpus. If you want to use only IDF, you're essentially 
focusing on the uniqueness of terms across documents without 
considering their frequency within a specific document.
Using only Inverse Document Frequency (IDF) without Term Frequency
(TF) is unconventional in the context of text vectorization for 
topic modeling or clustering because IDF on its own doesn't provide 
information about the term distribution within a specific document. 
It only gives information about how unique a term is across the entire 
corpus. However, if your goal is to focus solely on the uniqueness of 
terms across documents, you could manually compute IDF scores and use 
them as a form of vectorization.
What this script does is to load and preprocess transcripts, compute
the IDF values for each term, create IDF-only vectors for each document,
and perform KMeans clustering using these IDF vectors. The resulting
clusters are then mapped to the corresponding documents and saved in a JSON file.
"""

import os
import re
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import numpy as np

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
    directory = 'C:/Users/sirin/DATBAC-1/STG0006948/data/transcripts/CleanedTranscripts'
    preprocessed_texts, file_names = load_and_preprocess_transcripts(directory)

    # Using TfidfVectorizer to compute IDF values
    tfidf_vectorizer = TfidfVectorizer(use_idf=True, smooth_idf=True) 
    tfidf_vectorizer.fit_transform(preprocessed_texts)
    idf = tfidf_vectorizer.idf_
    feature_names = tfidf_vectorizer.get_feature_names_out()
    
    # Creating IDF-only vectors for each document
    idf_only_matrix = np.zeros((len(preprocessed_texts), len(feature_names)))
    for i, doc in enumerate(preprocessed_texts):
        tokens = doc.split()
        for token in tokens:
            if token in feature_names:
                idx = list(feature_names).index(token)
                idf_only_matrix[i][idx] = idf[idx]
                
    # Perform KMeans clustering
    num_clusters = 230
    km_model = KMeans(n_clusters=num_clusters)
    km_model.fit(idf_only_matrix)
    clusters = km_model.labels_.tolist()

    # Mapping documents to clusters
    topics_to_files = {}
    for i, cluster_label in enumerate(clusters):
        if cluster_label not in topics_to_files:
            topics_to_files[cluster_label] = []
        topics_to_files[cluster_label].append(file_names[i])

    # Saving the mappings to a JSON file
    with open('idf_kmeans_topic_mappings.json', 'w', encoding='utf-8') as f:
        json.dump(topics_to_files, f, ensure_ascii=False, indent=4)


