import os
import shutil
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# Function to read clean STM files
def read_stm_files(directory):
    stm_data = {}
    for filename in os.listdir(directory):
        if filename.endswith('.stm'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                stm_data[filename] = file.read()
    return stm_data

# Function to read BoW files
def read_bow_files(directory):
    bow_data = {}
    for filename in os.listdir(directory):
        if filename.endswith('bow_matrix.txt'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                bow_data[filename] = file.read()
    return bow_data

# Function to read n-gram (bigram/trigram) files
def read_ngram_files(directory):
    ngram_data = {}
    for filename in os.listdir(directory):
        if filename.endswith('bigrams.txt') or filename.endswith('trigrams.txt'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                ngram_data[filename] = file.read()
    return ngram_data

# Main clustering function
def cluster_transcripts(tfidf_matrix, bow_matrix, ngram_matrix, stm_data):
    # Combine TF-IDF matrix with BoW, bigram, and trigram data
    combined_matrix = np.hstack((tfidf_matrix.toarray(), bow_matrix.toarray(), ngram_matrix.toarray()))

    # Choose the number of clusters (you may need to experiment with this)
    num_clusters = 5

    # Apply K-means clustering
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    cluster_labels = kmeans.fit_predict(combined_matrix)

    # Evaluate clustering using silhouette score
    silhouette_avg = silhouette_score(combined_matrix, cluster_labels)
    print(f"Silhouette Score: {silhouette_avg}")

    # Create cluster folders
    for i in range(num_clusters):
        os.makedirs(f'cluster_{i}', exist_ok=True)

    # Move transcripts to cluster folders based on clustering results
    for filename, cluster_label in zip(stm_data.keys(), cluster_labels):
        shutil.move(filename, f'cluster_{cluster_label}/{filename}')

    print("Clustering completed.")

if __name__ == "__main__":
    # Directories containing all clean STM files, BoW files, and n-gram files
    stm_directory = 'clean_stm_files'
    ngram_directory = 'ngram_bow_files'
    bow_directory = 'bow_files'

    # Read clean STM data
    stm_data = read_stm_files(stm_directory)

    # Read BoW data
    bow_data = read_bow_files(bow_directory)

    # Read n-gram (bigram/trigram) data
    ngram_data = read_ngram_files(ngram_directory)

    # Vectorize STM data using TF-IDF
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(stm_data.values())

    # Vectorize BoW data using TF-IDF
    bow_vectorizer = TfidfVectorizer()
    bow_matrix = bow_vectorizer.fit_transform(bow_data.values())

    # Vectorize n-gram data using TF-IDF
    ngram_vectorizer = TfidfVectorizer()
    ngram_matrix = ngram_vectorizer.fit_transform(ngram_data.values())

    # Cluster transcripts
    cluster_transcripts(tfidf_matrix, bow_matrix, ngram_matrix, stm_data)
