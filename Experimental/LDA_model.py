import os
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import pandas as pd

# Set up NLTK resources
import nltk
nltk.download("punkt")
nltk.download("stopwords")

# Load stopwords and initialize lemmatizer
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

# Function to preprocess text
def preprocess_text(text):
    # Tokenize text
    tokens = word_tokenize(text.lower())
    # Remove stopwords and non-alphabetic tokens, and lemmatize
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token.isalpha() and token not in stop_words]
    return " ".join(tokens)

# Function to load and preprocess transcripts
def load_and_preprocess_transcripts(transcripts_dir):
    transcripts = []
    for root, dirs, files in os.walk(transcripts_dir):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            with open(file_path, "r", encoding="utf-8") as file:
                transcript = file.read()
                transcripts.append(transcript)
    # Preprocess transcripts
    preprocessed_transcripts = [preprocess_text(transcript) for transcript in transcripts]
    return preprocessed_transcripts

# Function to fit LDA model and assign topics
def fit_lda_and_assign_topics(transcripts, num_topics, category_words):
    # Convert transcripts to document-term matrix
    vectorizer = CountVectorizer()
    dtm = vectorizer.fit_transform(transcripts)
    
    # Fit LDA model
    lda = LatentDirichletAllocation(n_components=num_topics, random_state=42)
    lda.fit(dtm)
    
    # Assign transcripts to topics based on highest probability topic
    topic_assignments = lda.transform(dtm)
    transcript_topics = []
    transcript_probabilities = []
    for topic_probs in topic_assignments:
        topic_idx = topic_probs.argmax()
        # Choose a topic word from ted-topic.csv
        topic_word = category_words[topic_idx]
        transcript_topics.append(topic_word)
        transcript_probabilities.append(topic_probs.max())  # Probability score for the chosen topic
    
    return transcript_topics, transcript_probabilities

def read_category_words(category_words_file):
    df = pd.read_csv(category_words_file)
    category_words = df["ted_topic"].tolist()
    return category_words

if __name__ == "__main__":
    transcripts_dir = "Cluster_output_bag_of_words"
    num_topics = 364  # Specify the number of topics
    category_words_file = "Topics-Ted.csv"  # CSV file containing category words

    # Step 1: Load and preprocess transcripts
    transcripts = load_and_preprocess_transcripts(transcripts_dir)
    
    # Step 2: Read category words from CSV file
    category_words = read_category_words(category_words_file)

    # Step 3: Fit LDA model and assign topics
    transcript_topics, transcript_probabilities = fit_lda_and_assign_topics(transcripts, num_topics, category_words)
    
    # Step 4: Save results in a CSV file
    results_df = pd.DataFrame({"Transcript Number": range(1, len(transcripts) + 1),
                                "Category Word": transcript_topics,
                                "Probability": transcript_probabilities})
    results_df.to_csv("transcript_topicsLDA.csv", index=False)
