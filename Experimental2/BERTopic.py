import os
import re
from bertopic import BERTopic

"""
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
"""

def minimal_preprocess(text):
    # Adjusted preprocessing for BERTopic's usage
    cleaned_text = re.sub(r'.*<NA>\s?', '', text)
    cleaned_text = re.sub('<unk>', ' ', cleaned_text)
    cleaned_text = re.sub(r'\b\w{1,2}\b', '', cleaned_text)
    cleaned_text = re.sub('[^A-Za-z]+', ' ', cleaned_text).lower()
    return cleaned_text

def preprocess_and_tokenize(directory):
    # Load and preprocess transcripts
    processed_texts = []
    file_names = []
    for filename in os.listdir(directory):
        if filename.endswith('.stm'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                cleaned_text = minimal_preprocess(text)
                processed_texts.append(cleaned_text)
                file_names.append(filename)
    return processed_texts, file_names

if __name__ == '__main__':
    directory = '../data/TEDLIUM_release-3/TEDLIUM_release-3/data/stm'
    transcripts, file_names = preprocess_and_tokenize(directory)

    # Initialize BERTopic
    topic_model = BERTopic(language="english", calculate_probabilities=False, verbose=True)
    topics, _ = topic_model.fit_transform(transcripts)

    # Save the model and topics
    topic_model.save("bertopic_model")

    # Organize filenames by topics
    topics_to_filenames = {}
    for filename, topic in zip(file_names, topics):
        if topic in topics_to_filenames:
            topics_to_filenames[topic].append(filename)
        else:
            topics_to_filenames[topic] = [filename]
    
        # Print topics, their top word as the topic name, and associated filenames
    print("\nPrinting topics with associated transcripts for easier review:\n")
    for topic in sorted(topics_to_filenames.keys()):
        # Get top words for the topic
        topic_words = topic_model.get_topic(topic)
        if topic_words:  # Check if there are words for the topic
            # Extract the top word
            top_word = topic_words[0][0]  # This gets the top word (highest score)
            print(f"\nTopic '{topic}' (Top word: {top_word}):")
            for filename in topics_to_filenames[topic]:
                print(f" - {filename}")
        else:
            print(f"\nTopic '{topic}' (No top words found):")
            for filename in topics_to_filenames[topic]:
                print(f" - {filename}")

