import os
import numpy as np
import pandas as pd
from lda2vec.Lda2vec import Lda2vec as Lda2Vec
from gensim.models.word2vec import Word2Vec
from gensim.corpora import Dictionary
from gensim.utils import simple_preprocess
import tensorflow as tf

# Function to read transcripts from STM files
def read_stm_files(directory):
    transcripts = []
    for filename in os.listdir(directory):
        if filename.endswith(".stm"):
            with open(os.path.join(directory, filename), 'r') as file:
                transcript = file.read()
                transcripts.append(transcript)
    return transcripts

# Preprocess the transcripts
def preprocess_transcripts(transcripts):
    processed_transcripts = []
    for transcript in transcripts:
        processed_transcript = simple_preprocess(transcript)
        processed_transcripts.append(processed_transcript)
    return processed_transcripts

# Train Lda2vec model
def train_lda2vec_model(processed_transcripts):
    dictionary = Dictionary(processed_transcripts)
    corpus = [dictionary.doc2bow(text) for text in processed_transcripts]

    # Calculate the number of unique documents and vocabulary size
    num_unique_documents = len(corpus)
    vocab_size = len(dictionary)

    # Train Word2Vec model
    w2v_model = Word2Vec(processed_transcripts, vector_size=100, window=5, min_count=1, workers=4)

    # Initialize Lda2Vec model
    lda2vec_model = Lda2Vec(num_unique_documents=num_unique_documents, vocab_size=vocab_size, num_topics=10,
                             pretrained_embeddings=w2v_model.wv.vectors)
    lda2vec_model.fit(w2v_model, corpus, dictionary)
    return lda2vec_model

# Assign topics to transcripts
def assign_topics(lda2vec_model, processed_transcripts):
    topic_assignments = []
    for transcript in processed_transcripts:
        bow = lda2vec_model.id2word.doc2bow(transcript)
        topics = lda2vec_model[bow]
        dominant_topic = max(topics, key=lambda x: x[1])[0]
        topic_assignments.append(dominant_topic)
    return topic_assignments

# Output results to CSV
def output_to_csv(topic_assignments, output_file):
    df = pd.DataFrame({'Transcript Number': range(1, len(topic_assignments)+1), 'Topic Assigned': topic_assignments})
    df.to_csv(output_file, index=False)

# Main function
def main():
    # Read transcripts
    transcripts_directory = "cleaned_Devtranscripts"
    transcripts = read_stm_files(transcripts_directory)

    # Preprocess transcripts
    processed_transcripts = preprocess_transcripts(transcripts)

    # Train Lda2vec model
    lda2vec_model = train_lda2vec_model(processed_transcripts)

    # Assign topics
    topic_assignments = assign_topics(lda2vec_model, processed_transcripts)

    # Output results to CSV
    output_file = "topic_assignments.csv"
    output_to_csv(topic_assignments, output_file)

if __name__ == "__main__":
    main()
