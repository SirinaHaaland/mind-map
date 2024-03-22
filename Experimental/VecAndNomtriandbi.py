import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
import numpy as np
import shutil


def read_files(directory):
    files_data = {}
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                files_data[filename] = file.readlines()
    return files_data


def tfidf_vectorize_normalize(data):
    tfidf_vectorizer = TfidfVectorizer()
    X = tfidf_vectorizer.fit_transform(data)
    scaler = StandardScaler()
    X_normalized = scaler.fit_transform(X.toarray())
    return np.array(X_normalized)


def copy_bow_files(input_directory, output_directory):
    bow_files = [filename for filename in os.listdir(input_directory) if filename.endswith('bow_matrix.txt')]
    for bow_file in bow_files:
        shutil.copy(os.path.join(input_directory, bow_file), output_directory)


def main():
    input_directory = 'ngram_bow_files'

    output_directory = 'combined_files'
    os.makedirs(output_directory, exist_ok=True)

    copy_bow_files(input_directory, output_directory)

    files_data = read_files(input_directory)


    bigram_files = {filename: content for filename, content in files_data.items() if 'bigrams.txt' in filename}
    trigram_files = {filename: content for filename, content in files_data.items() if 'trigrams.txt' in filename}

    for bigram_filename, bigram_content in bigram_files.items():
        vectorized_normalized_data = tfidf_vectorize_normalize(bigram_content)
        np.savetxt(os.path.join(output_directory, bigram_filename), vectorized_normalized_data, delimiter=',')

    for trigram_filename, trigram_content in trigram_files.items():
        vectorized_normalized_data = tfidf_vectorize_normalize(trigram_content)
        np.savetxt(os.path.join(output_directory, trigram_filename), vectorized_normalized_data, delimiter=',')

    print("TF-IDF vectorization and normalization completed. Files saved in the output directory.")

if __name__ == "__main__":
    main()

