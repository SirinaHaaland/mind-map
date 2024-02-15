import os
import shutil
import numpy as np
import csv
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

# Function to read clean STM files
def read_stm_files(directory):
    stm_data = {}
    for filename in os.listdir(directory):
        if filename.endswith('.stm'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                stm_data[filename] = file.read()
    return stm_data

def read_categories_from_csv(csv_file):
    categories = []
    with open(csv_file, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            categories.extend(row)
    return categories

def analyze_clusters(cluster_directory, categories):
    num_topics = len(categories)
    for cluster_folder in os.listdir(cluster_directory):
        cluster_path = os.path.join(cluster_directory, cluster_folder)
        if os.path.isdir(cluster_path) and cluster_folder.startswith('cluster'):
            cluster_id = cluster_folder.split('_')[1]
            cluster_stm_files = read_stm_files(cluster_path)
            documents = list(cluster_stm_files.values())
            vectorizer = CountVectorizer()
            X = vectorizer.fit_transform(documents)
            lda = LatentDirichletAllocation(n_components=num_topics, random_state=42)
            lda.fit(X)
            top_topic = np.argmax(lda.components_)
            if top_topic < len(categories):
                category = categories[top_topic]
                score = lda.components_[0][top_topic]
                new_folder_name = f'cluster_{cluster_id}_{category}'
                new_cluster_path = os.path.join(cluster_directory, new_folder_name)
                os.rename(cluster_path, new_cluster_path)
                print(f"Cluster {cluster_id}: {len(documents)} STM files analyzed. Topic: {category}, Score: {score:.2f}")
            else:
                print(f"Cluster {cluster_id}: {len(documents)} STM files analyzed. No suitable topic found.")

if __name__ == "__main__":
    # Directory containing cluster folders
    cluster_directory = '_Cluster'

    # CSV file containing categories
    categories_csv_file = 'Topics-Ted.csv'

    # Read categories from CSV
    categories = read_categories_from_csv(categories_csv_file)

    # Analyze clusters and assign topics
    analyze_clusters(cluster_directory, categories)
