import os
import shutil
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

def read_stm_files(directory):
    stm_data = {}
    for filename in os.listdir(directory):
        if filename.endswith('.stm'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                stm_data[filename] = file.read()
    return stm_data

def read_ngram_files(directory):
    ngram_data = {}
    for filename in os.listdir(directory):
        if filename.endswith('pca.txt'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read().strip()
                if content:
                    try:
                        ngram_data[filename] = np.loadtxt(file_path, delimiter=',')
                    except ValueError:
                        print(f"Error: Invalid data in file {filename}. Skipping.")
                else:
                    print(f"Error: Empty file {filename}. Skipping.")
    return ngram_data

def find_optimal_clusters(data, max_clusters=10):
    silhouette_scores = []
    for i in range(2, max_clusters + 1):
        kmeans = KMeans(n_clusters=i, random_state=42)
        cluster_labels = kmeans.fit_predict(data)
        silhouette_avg = silhouette_score(data, cluster_labels)
        silhouette_scores.append(silhouette_avg)
    optimal_num_clusters = silhouette_scores.index(max(silhouette_scores)) + 2 
    return optimal_num_clusters

def pad_matrices(matrices):
    max_rows = max(matrix.shape[0] for matrix in matrices)
    padded_matrices = [np.pad(matrix, ((0, max_rows - matrix.shape[0]), (0, 0)), mode='constant') for matrix in matrices]
    return padded_matrices

def cluster_transcripts(ngram_data, stm_data, num_clusters):
    if not ngram_data:
        print("Error: No n-gram data found.")
        return
    ngram_matrices = [matrix for matrix in ngram_data.values()]

    if not ngram_matrices:
        print("Error: No valid n-gram matrices found.")
        return
    padded_matrices = pad_matrices(ngram_matrices)
    combined_matrix = np.hstack(padded_matrices)

    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    cluster_labels = kmeans.fit_predict(combined_matrix)

    cluster_directory = '_Cluster'
    os.makedirs(cluster_directory, exist_ok=True)


    total_stm_files = 0
    for filename, cluster_label in zip(stm_data.keys(), cluster_labels):
        src_path = os.path.join(stm_directory, filename)
        dst_directory = os.path.join(cluster_directory, f'cluster_{cluster_label}')
        os.makedirs(dst_directory, exist_ok=True)
        dst_path = os.path.join(dst_directory, filename)
        shutil.copy(src_path, dst_path)
        total_stm_files += 1

    print(f"Total .stm files placed in clusters: {total_stm_files}")
    print("Clustering completed.")

if __name__ == "__main__":
    stm_directory = 'cleaned_transcripts'
    bigram_trigram_directory = 'dimensionality_reduced_files'

    stm_data = read_stm_files(stm_directory)
    ngram_data = read_ngram_files(bigram_trigram_directory)
    padded_matrices = pad_matrices([matrix for matrix in ngram_data.values()])
    combined_matrix = np.hstack(padded_matrices)

    num_clusters = find_optimal_clusters(combined_matrix)
    cluster_transcripts(ngram_data, stm_data, num_clusters)
