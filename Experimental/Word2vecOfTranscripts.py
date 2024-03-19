import os
import re
import gensim
from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import logging
import nltk


logging.basicConfig(format="%(levelname)s - %(message)s", level=logging.INFO)
nltk.download("punkt")
nltk.download("stopwords")
stop_words = set(stopwords.words("english"))

def preprocess_text(text):
    text = re.sub(r"[^a-zA-Z0-9]", " ", text.lower())
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stop_words]
    return tokens

def process_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
        tokens = preprocess_text(text)
    return tokens

def create_word2vec_model(input_dir, output_path):
    model = Word2Vec(min_count=1, workers=3)
    all_tokens = []
    for root, dirs, files in os.walk(input_dir):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            tokens = process_file(file_path)
            all_tokens.append(tokens)

    model.build_vocab(all_tokens)
    model.train(all_tokens, total_examples=model.corpus_count, epochs=10)
    model.save(output_path)
    logging.info(f"Word2Vec model saved to {output_path}")

if __name__ == "__main__":
    input_dir = "cleaned_Devtranscripts"
    output_path = "word2vec_modelDevt.bin"
    create_word2vec_model(input_dir, output_path)
