import os
import torch
from transformers import BertModel, BertTokenizer
import nltk
import numpy as np
from sklearn.cluster import KMeans
from yellowbrick.cluster import KElbowVisualizer

nltk.download('wordnet')

# Function to read STM files from a directory
def read_stm_files(directory):
    stm_files = []
    for filename in os.listdir(directory):
        if filename.endswith('.stm'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                stm_content = file.read()
                stm_files.append(stm_content)
    return stm_files

# Function to preprocess transcripts and generate document embeddings
def preprocess_and_embed(transcripts):
    model_name = 'bert-base-uncased'
    tokenizer = BertTokenizer.from_pretrained(model_name)
    bert_model = BertModel.from_pretrained(model_name)

    document_embeddings = []
    for transcript in transcripts:
        # Tokenize the transcript
        tokenized_transcript = tokenizer.tokenize(transcript)
        
        # Split the transcript into chunks of maximum length
        max_length = tokenizer.model_max_length
        chunked_transcript = [tokenized_transcript[i:i + max_length] for i in range(0, len(tokenized_transcript), max_length)]

        # Generate embeddings for each chunk
        chunk_embeddings = []
        for chunk in chunked_transcript:
            input_ids = torch.tensor(tokenizer.convert_tokens_to_ids(chunk)).unsqueeze(0)
            with torch.no_grad():
                outputs = bert_model(input_ids)
                last_hidden_states = outputs.last_hidden_state
            chunk_embeddings.append(last_hidden_states.mean(dim=1).squeeze().numpy())
        
        # Combine embeddings of chunks
        document_embeddings.append(np.mean(chunk_embeddings, axis=0))
    
    return document_embeddings

# Function to perform clustering and assign topics
def perform_clustering(document_embeddings, num_topics=5):
    kmeans = KMeans(n_clusters=num_topics)
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
    # Directory containing STM files
    directory = 'cleaned_Devtranscripts'

    # Output directory for cluster STM files
    output_directory = 'cluster_stm_files'
    os.makedirs(output_directory, exist_ok=True)

    # Read all STM files from the directory
    stm_transcripts = read_stm_files(directory)

    if not stm_transcripts:
        print("No STM files found in the directory.")
        return

    # Preprocess and generate document embeddings
    document_embeddings = preprocess_and_embed(stm_transcripts)
    document_embeddings = np.array(document_embeddings)  # Convert to numpy array

    # Determine the optimal number of clusters using the elbow method
    model = KMeans()
    # Adjust the range of cluster numbers based on the number of samples
    num_samples = len(stm_transcripts)
    visualizer = KElbowVisualizer(model, k=(2, min(2*num_samples, 800)))
    visualizer.fit(document_embeddings)
    visualizer.show()
    
    # Choose the optimal number of clusters based on the elbow method
    num_clusters = visualizer.elbow_value_
    print("Optimal number of clusters:", num_clusters)

    # Perform clustering and assign topics
    cluster_labels = perform_clustering(document_embeddings, num_clusters)

    # Save transcripts belonging to the same cluster in a single STM file
    save_cluster_stm_files(stm_transcripts, cluster_labels, output_directory)

    print("Cluster STM files saved successfully.")

if __name__ == "__main__":
    main()
