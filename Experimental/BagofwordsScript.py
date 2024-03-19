import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd

import nltk
nltk.download("punkt")
nltk.download("stopwords")

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token.isalpha() and token not in stop_words]
    return " ".join(tokens)

def create_bag_of_words(transcript):
    preprocessed_text = preprocess_text(transcript)
    vectorizer = CountVectorizer()
    bag_of_words = vectorizer.fit_transform([preprocessed_text])
    feature_names = vectorizer.get_feature_names_out()
    bag_of_words_df = pd.DataFrame(bag_of_words.toarray(), columns=feature_names)
    return bag_of_words_df

if __name__ == "__main__":
    transcripts_dir = "cluster_stm_files"
    output_dir = "Cluster_output_bag_of_words"

    for root, dirs, files in os.walk(transcripts_dir):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            with open(file_path, "r", encoding="utf-8") as file:
                transcript = file.read()
                bag_of_words_df = create_bag_of_words(transcript)
                output_file_path = os.path.join(output_dir, f"{os.path.splitext(file_name)[0]}_bag_of_words.csv")
                bag_of_words_df.to_csv(output_file_path, index=False)
