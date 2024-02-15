import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
import numpy as np
import shutil

# Function to read n-gram files and BoW file
def read_files(directory):
    files_data = {}
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                files_data[filename] = file.readlines()
    return files_data

# Function to perform TF-IDF vectorization and normalization
def tfidf_vectorize_normalize(data):
    tfidf_vectorizer = TfidfVectorizer()
    X = tfidf_vectorizer.fit_transform(data)
    scaler = StandardScaler()
    X_normalized = scaler.fit_transform(X.toarray())
    return np.array(X_normalized)

# Function to copy BoW matrix files from input directory to output directory
def copy_bow_files(input_directory, output_directory):
    bow_files = [filename for filename in os.listdir(input_directory) if filename.endswith('bow_matrix.txt')]
    for bow_file in bow_files:
        shutil.copy(os.path.join(input_directory, bow_file), output_directory)

# Main function
def main():
    # Input directory containing all files
    input_directory = 'ngram_bow_files'

    # Output directory for combined files
    output_directory = 'combined_files'
    os.makedirs(output_directory, exist_ok=True)

    # Copy BoW matrix files to output directory
    copy_bow_files(input_directory, output_directory)

    # Read all n-gram files
    files_data = read_files(input_directory)

    # Separate n-gram files based on their types (bigram or trigram)
    bigram_files = {filename: content for filename, content in files_data.items() if 'bigrams.txt' in filename}
    trigram_files = {filename: content for filename, content in files_data.items() if 'trigrams.txt' in filename}

    # Perform TF-IDF vectorization and normalization for bigram files
    for bigram_filename, bigram_content in bigram_files.items():
        vectorized_normalized_data = tfidf_vectorize_normalize(bigram_content)
        np.savetxt(os.path.join(output_directory, bigram_filename), vectorized_normalized_data, delimiter=',')

    # Perform TF-IDF vectorization and normalization for trigram files
    for trigram_filename, trigram_content in trigram_files.items():
        vectorized_normalized_data = tfidf_vectorize_normalize(trigram_content)
        np.savetxt(os.path.join(output_directory, trigram_filename), vectorized_normalized_data, delimiter=',')

    print("TF-IDF vectorization and normalization completed. Files saved in the output directory.")

if __name__ == "__main__":
    main()

