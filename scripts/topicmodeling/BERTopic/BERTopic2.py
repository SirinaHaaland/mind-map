import os
import json
from bertopic import BERTopic

def preprocess(directory):
    # Load and preprocess transcripts
    processed_texts = []
    file_names = []
    for filename in os.listdir(directory):
        if filename.endswith('.stm'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read() #reads the full text of each file
                processed_texts.append(text)
                file_names.append(filename)
    return processed_texts, file_names

if __name__ == '__main__':
    directory = '../../../data/transcripts/CleanedTranscripts'
    transcripts, file_names = preprocess(directory)

    # Initialize BERTopic
    # min_topic_size=5: minimum number of documents in a topic
    # not possible to set maximum number of documents in a topic
    # nr_topics=230: number of topics to find, has no effect
    topic_model = BERTopic(language="english", n_gram_range=(1, 2), min_topic_size=5, nr_topics=230)

    topics, _ = topic_model.fit_transform(transcripts)

    # Save the model and topics
    topic_model.save("bertopic_model")

    # Organize filenames by topics
    topics_to_filenames = {}
    for filename, topic in zip(file_names, topics):
        topic_words = topic_model.get_topic(topic)
        if topic_words:
            top_word = topic_words[0][0]  # Get the top word for the topic
            if top_word not in topics_to_filenames:
                topics_to_filenames[top_word] = []
            topics_to_filenames[top_word].append(filename)
    
    with open('bert_topic2_mappings.json', 'w', encoding='utf-8') as f:
        json.dump(topics_to_filenames, f, ensure_ascii=False, indent=4)
    
    for top_word, filenames in topics_to_filenames.items():
        print(f"\nTopic (Top word: {top_word}):")
        for filename in filenames:
            print(f" - {filename}")


