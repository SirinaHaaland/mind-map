import os
import re
import gensim
from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import logging

# Set up logging
logging.basicConfig(format="%(levelname)s - %(message)s", level=logging.INFO)

# Download NLTK resources
import nltk
nltk.download("punkt")
nltk.download("stopwords")

# Set up NLTK stopwords
stop_words = set(stopwords.words("english"))

# Function to preprocess text
def preprocess_text(text):
    # Remove non-alphanumeric characters and convert to lowercase
    text = re.sub(r"[^a-zA-Z0-9]", " ", text.lower())
    # Tokenize text
    tokens = word_tokenize(text)
    # Remove stop words
    tokens = [word for word in tokens if word not in stop_words]
    return tokens

# Function to read and preprocess files
def process_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
        tokens = preprocess_text(text)
    return tokens

# Function to create Word2Vec model
def create_word2vec_model(input_dir, output_path):
    # Initialize Word2Vec model
    model = Word2Vec(min_count=1, workers=3)

    # Collect all tokens from files in input directory
    all_tokens = []
    for root, dirs, files in os.walk(input_dir):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            # Process each file
            tokens = process_file(file_path)
            all_tokens.append(tokens)

    # Build vocabulary using all tokens
    model.build_vocab(all_tokens)

    # Train Word2Vec model
    model.train(all_tokens, total_examples=model.corpus_count, epochs=10)

    # Save Word2Vec model
    model.save(output_path)
    logging.info(f"Word2Vec model saved to {output_path}")

if __name__ == "__main__":
    input_dir = "cleaned_Devtranscripts"
    output_path = "word2vec_modelDevt.bin"
    create_word2vec_model(input_dir, output_path)
