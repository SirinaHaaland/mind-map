import os
import numpy as np
from sklearn.decomposition import PCA

# Function to read tri and bi files
def read_files(directory):
    files_data = {}
    for filename in os.listdir(directory):
        if filename.endswith('trigrams.txt') or filename.endswith('bigrams.txt'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                file_content = file.readlines()
                files_data[filename[:-4]] = file_content
    return files_data

# Function to perform PCA dimensionality reduction
def perform_pca(data, n_components=2):
    # Check if the input data is empty
    if len(data) == 0:
        print("Error: Empty array provided.")
        return None

    # Check if the input data is 1D, reshape it if necessary
    if data.ndim == 1:
        data = data.reshape(-1, 1)

    pca = PCA(n_components=n_components)
    pca_result = pca.fit_transform(data)

    # Check if the result is empty or 0D array
    if pca_result.size == 0:
        print("Error: PCA result is empty.")
        return None

    return pca_result


# Main function
def main():
    # Directory containing tri and bi files
    directory = 'combined_files'

    # Output directory for dimensionality-reduced files
    output_directory = 'dimensionality_reduced_files'
    os.makedirs(output_directory, exist_ok=True)

    # Read tri and bi files
    files_data = read_files(directory)

    if not files_data:
        print("No tri and bi files found in the directory.")
        return

    # Perform PCA dimensionality reduction for each file
    for file_name, file_content in files_data.items():
        # Convert text data to numpy array
        data = []
        for line in file_content:
            try:
                if line.strip():  # Skip empty lines
                    data.append(list(map(float, line.strip().split(','))))
            except ValueError:
                print(f"Error converting line to float in file {file_name}. Skipping line.")

        data = np.array(data)

        # Perform PCA dimensionality reduction
        pca_result = perform_pca(data)

        if pca_result is None:  # Check if pca_result is None
            print(f"Warning: PCA result is None for file {file_name}. Skipping saving.")
            continue

        if pca_result.size == 0:  # Check if pca_result is empty
            print(f"Warning: PCA result is empty for file {file_name}. Skipping saving.")
            continue

        # Save dimensionality-reduced representation
        output_file_path = os.path.join(output_directory, f'{file_name}_pca.txt')
        np.savetxt(output_file_path, pca_result, delimiter=',')

    print("Dimensionality-reduced files saved successfully.")

if __name__ == "__main__":
    main()
