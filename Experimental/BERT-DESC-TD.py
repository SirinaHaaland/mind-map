import os
import torch
from transformers import BertModel, BertTokenizer
import numpy as np
from sklearn.cluster import KMeans
from yellowbrick.cluster import KElbowVisualizer

# Function to read bigram or trigram files
def read_ngram_files(directory):
    ngram_data = {}
    for filename in os.listdir(directory):
        if filename.endswith('pca.txt'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read().strip()
                if content:
                    try:
                        # Convert the string content to a 2D array
                        ngram_data[filename] = np.loadtxt(file_path, delimiter=',')
                    except ValueError:
                        print(f"Error: Invalid data in file {filename}. Skipping.")
                else:
                    print(f"Error: Empty file {filename}. Skipping.")
    return ngram_data

# Function to preprocess transcripts and generate document embeddings
def preprocess_and_embed(transcripts):
    model_name = 'bert-base-uncased'
    tokenizer = BertTokenizer.from_pretrained(model_name)
    bert_model = BertModel.from_pretrained(model_name)

    max_length = 512  # Maximum length for BERT input
    
    document_embeddings = []
    for transcript in transcripts:
        # Tokenize the transcript
        tokenized_transcript = tokenizer.tokenize(transcript)
        
        # Truncate or pad tokenized transcript to max_length
        tokenized_transcript = tokenized_transcript[:max_length] + ['[PAD]'] * (max_length - len(tokenized_transcript))
        
        input_ids = torch.tensor(tokenizer.convert_tokens_to_ids(tokenized_transcript)).unsqueeze(0)
        with torch.no_grad():
            outputs = bert_model(input_ids)
            last_hidden_states = outputs.last_hidden_state
        
        # Get embedding for the first token (CLS token)
        document_embedding = last_hidden_states[:, 0, :].squeeze().numpy()
        document_embeddings.append(document_embedding)
    
    return document_embeddings


# Function to perform clustering and assign topics
def perform_clustering(document_embeddings, num_clusters):
    kmeans = KMeans(n_clusters=num_clusters)
    cluster_labels = kmeans.fit_predict(document_embeddings)
    return cluster_labels

# Function to save transcripts belonging to the same cluster in a single STM file
def save_cluster_stm_files(stm_transcripts, cluster_labels, output_directory):
    for cluster_num in np.unique(cluster_labels):
        cluster_indices = np.where(cluster_labels == cluster_num)[0]
        cluster_transcripts = [stm_transcripts[i] for i in cluster_indices]
        cluster_stm_content = '\n'.join(cluster_transcripts)
        
        # Write cluster transcripts to STM file
        output_file_path = os.path.join(output_directory, f'cluster_{cluster_num}.stm')
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(cluster_stm_content)

# Main function
def main():
    # Directories containing bigram and trigram files
    bigram_trigram_directory = 'dimensionality_reduced_files'

    # Output directory for cluster STM files
    output_directory = 'cluster_stm_files'
    os.makedirs(output_directory, exist_ok=True)

    # Read bigram and trigram files
    ngram_data = read_ngram_files(bigram_trigram_directory)

    # Extract transcripts corresponding to the bigram and trigram files
    transcripts = [filename.split('_')[0] + '.stm' for filename in ngram_data.keys()]

    if not transcripts:
        print("No transcripts found corresponding to the bigram and trigram files.")
        return

    # Preprocess and generate document embeddings
    document_embeddings = preprocess_and_embed(transcripts)
    document_embeddings = np.array(document_embeddings)  # Convert to numpy array

    # Determine the optimal number of clusters using the elbow method
    model = KMeans()
    visualizer = KElbowVisualizer(model, k=(2, 2350))
    visualizer.fit(document_embeddings)
    visualizer.show()
    
    # Choose the optimal number of clusters based on the elbow method
    num_clusters = visualizer.elbow_value_
    print("Optimal number of clusters:", num_clusters)

    # Perform clustering and assign topics
    cluster_labels = perform_clustering(document_embeddings, num_clusters)

    # Save transcripts belonging to the same cluster in a single STM file
    save_cluster_stm_files(transcripts, cluster_labels, output_directory)

    print("Cluster STM files saved successfully.")


if __name__ == "__main__":
    main()
