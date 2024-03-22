import os
import numpy as np
from sklearn.decomposition import PCA

def read_files(directory):
    files_data = {}
    for filename in os.listdir(directory):
        if filename.endswith('trigrams.txt') or filename.endswith('bigrams.txt'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                file_content = file.readlines()
                files_data[filename[:-4]] = file_content
    return files_data

def perform_pca(data, n_components=2):
    if len(data) == 0:
        print("Error: Empty array provided.")
        return None

    if data.ndim == 1:
        data = data.reshape(-1, 1)

    pca = PCA(n_components=n_components)
    pca_result = pca.fit_transform(data)

    if pca_result.size == 0:
        print("Error: PCA result is empty.")
        return None

    return pca_result


def main():
    directory = 'combined_files'

    output_directory = 'dimensionality_reduced_files'
    os.makedirs(output_directory, exist_ok=True)

    files_data = read_files(directory)

    if not files_data:
        print("No tri and bi files found in the directory.")
        return

    for file_name, file_content in files_data.items():
        data = []
        for line in file_content:
            try:
                if line.strip(): 
                    data.append(list(map(float, line.strip().split(','))))
            except ValueError:
                print(f"Error converting line to float in file {file_name}. Skipping line.")

        data = np.array(data)
        pca_result = perform_pca(data)

        if pca_result is None: 
            print(f"Warning: PCA result is None for file {file_name}. Skipping saving.")
            continue

        if pca_result.size == 0:
            print(f"Warning: PCA result is empty for file {file_name}. Skipping saving.")
            continue

        output_file_path = os.path.join(output_directory, f'{file_name}_pca.txt')
        np.savetxt(output_file_path, pca_result, delimiter=',')

    print("Dimensionality-reduced files saved successfully.")

if __name__ == "__main__":
    main()
