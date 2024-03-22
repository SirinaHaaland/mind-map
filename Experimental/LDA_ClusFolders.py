import os
import shutil
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def preprocess_text(text):
    # Tokenize
    tokens = word_tokenize(text.lower())

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [token for token in tokens if token not in stop_words]

    # Lemmatize
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]

    # Remove tokens with length <= 2
    final_tokens = [token for token in lemmatized_tokens if len(token) > 2]

    return " ".join(final_tokens)

def read_cleaned_transcript(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return preprocess_text(file.read())

def read_stm_file(file_path, cleaned_transcript_directory):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read().strip().split('\n')
        filenames = [filename.split('_')[0] for filename in content]  # Extract name before underscore
        filenames = [filename.split('.')[0] for filename in filenames]  # Remove .stm extension

        all_transcripts = []
        for prefix in filenames:
            transcript_files = [file for file in os.listdir(cleaned_transcript_directory) if file.startswith(prefix)]
            for transcript_file in transcript_files:
                transcript_file_path = os.path.join(cleaned_transcript_directory, transcript_file)
                transcript = read_cleaned_transcript(transcript_file_path)
                all_transcripts.append(transcript)
        return all_transcripts

def fit_lda_and_assign_topics(transcripts, num_topics, category_words):
    vectorizer = CountVectorizer()
    dtm = vectorizer.fit_transform(transcripts)
    
    lda = LatentDirichletAllocation(n_components=num_topics, random_state=42)
    lda.fit(dtm)
    
    topic_assignments = lda.transform(dtm)
    transcript_topics = []
    transcript_probabilities = []
    for topic_probs in topic_assignments:
        topic_idx = topic_probs.argmax()
        topic_word = category_words[topic_idx]
        transcript_topics.append(topic_word)
        transcript_probabilities.append(topic_probs.max())
    
    return transcript_topics, transcript_probabilities

def process_cluster(cluster_directory, cleaned_transcript_directory, ted_talks_csv):
    print(f"Cluster directory: {cluster_directory}")
    print(f"Cleaned transcript directory: {cleaned_transcript_directory}")
    print(f"TED Talks CSV: {ted_talks_csv}")

    ted_talks_df = pd.read_csv(ted_talks_csv)
    categories = set(ted_talks_df['ted_topic'].tolist())

    print("Entering the loop to process clusters...")

    for stm_file in os.listdir(cluster_directory):
        if stm_file.endswith('.stm'):
            print(f"Processing cluster: {stm_file}")
            stm_file_path = os.path.join(cluster_directory, stm_file)

            all_transcripts = read_stm_file(stm_file_path, cleaned_transcript_directory)

            if not all_transcripts:
                print("No transcripts found for this cluster.")
                continue

            # Apply LDA and assign topics
            transcript_topics, _ = fit_lda_and_assign_topics(all_transcripts, num_topics=5, category_words=list(categories))
            top_category = max(set(transcript_topics), key=transcript_topics.count)

            cluster_number = stm_file.split('_')[1].split('.')[0]  # Extract cluster number

            # Rename the file to the format cluster_nr_category.stm
            new_cluster_file = f"{cluster_number}_{top_category}.stm"
            new_cluster_file_path = os.path.join(cluster_directory, new_cluster_file)

            # Check if the new file name already exists, if it does, add a suffix
            suffix = 1
            while os.path.exists(new_cluster_file_path):
                new_cluster_file = f"{cluster_number}_{top_category}_{suffix}.stm"
                new_cluster_file_path = os.path.join(cluster_directory, new_cluster_file)
                suffix += 1

            os.rename(stm_file_path, new_cluster_file_path)

            print(f"Cluster {stm_file} processed successfully.")

def main():
    # Directory containing cluster files (STM files)
    cluster_directory = 'cluster_stm_files'
    # Directory containing cleaned transcript files
    cleaned_transcript_directory = 'cleaned_transcripts'
    # Path to TED Talks CSV file
    ted_talks_csv = 'Topics-Ted.csv'

    process_cluster(cluster_directory, cleaned_transcript_directory, ted_talks_csv)

    print("All clusters processed successfully.")

if __name__ == "__main__":
    main()
