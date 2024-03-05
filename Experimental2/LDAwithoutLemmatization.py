import os
import re
import json
from gensim import corpora, models
import gensim
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from gensim.models.coherencemodel import CoherenceModel
from gensim.models import Phrases
from gensim.models.phrases import Phraser
"""
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
"""
def minimal_preprocess(text):
    # Basic cleaning and tokenization for phrase detection
    cleaned_text = re.sub(r'.*<NA>\s?', '', text)
    cleaned_text = re.sub('<unk>', ' ', cleaned_text)
    cleaned_text = re.sub(r'\b\w{1,2}\b', '', cleaned_text)
    cleaned_text = re.sub('[^A-Za-z]+', ' ', cleaned_text)
    tokens = word_tokenize(cleaned_text.lower())
    return tokens

def train_phrases(transcripts):
    # Train the Phrases model to detect common phrases (bigrams or more)
    phrases = Phrases(transcripts, min_count=5, threshold=10)
    bigram = Phraser(phrases)
    return bigram

def preprocess(tokens, bigram_model):
    # Apply the Phrases model to merge detected phrases into single tokens
    tokens_with_phrases = bigram_model[tokens]
    # Continue with your preprocessing (stopwords removal, lemmatization, etc.)
    with open('stopwords.txt', 'r', encoding='utf-8') as file:
        stop_words = set(file.read().splitlines())
    processed_tokens = [w for w in tokens_with_phrases if w not in stop_words]
    return processed_tokens

def load_and_preprocess_transcripts(directory):
    # First pass: collect minimally processed transcripts for phrase model training
    minimal_transcripts = []
    file_names = []
    for filename in os.listdir(directory):
        if filename.endswith('.stm'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                minimal_tokens = minimal_preprocess(text)
                minimal_transcripts.append(minimal_tokens)
                file_names.append(filename)
    
    bigram_model = train_phrases(minimal_transcripts)
    
    processed_transcripts = [preprocess(tokens, bigram_model) for tokens in minimal_transcripts]
    
    return processed_transcripts, file_names

if __name__ == '__main__':  
    #directory = '../data/TEDLIUM_release-3/TEDLIUM_release-3/legacy/test/randomtestscripts'
    directory = '../data/TEDLIUM_release-3/TEDLIUM_release-3/data/stm'
    transcripts, file_names = load_and_preprocess_transcripts(directory)

    dictionary = corpora.Dictionary(transcripts)
    corpus = [dictionary.doc2bow(text) for text in transcripts]
    # Save processed transcripts for future use (commented out for testing)
    """
    processed_transcripts = {'filename': text for filename, text in zip(file_names, transcripts)}
    with open('processed_transcripts.json', 'w') as f:
        json.dump(processed_transcripts, f)
    """
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=300, id2word=dictionary, passes=15)

    coherence_model_lda = CoherenceModel(model=ldamodel, texts=transcripts, dictionary=dictionary, coherence='c_v')
    coherence_lda = coherence_model_lda.get_coherence()
    print('\nCoherence Score:\n ', coherence_lda) 

    # Extracting the most significant topic for each transcript and assigning that topic to the transcript 
    topic_assignments = {file_names[i]: max(ldamodel[corpus[i]], key=lambda x: x[1])[0] for i in range(len(file_names))}
    # Save the topic assignments (commented out for testing)
    """
    with open('topic_assignments.json', 'w') as f:
        json.dump(topic_assignments, f)
    """
    # Generate full topic descriptions (to print/see the words in each topic, not just topic id))
    full_topic_descriptions = {i: ldamodel.show_topic(i) for i in range(ldamodel.num_topics)}

    # Simplify/reduce topics to one (the most significant) word
    simplified_topics = {}
    for topic_id in range(ldamodel.num_topics):
        word_id, _ = max(ldamodel.get_topic_terms(topic_id), key=lambda x: x[1])
        simplified_topics[topic_id] = ldamodel.id2word[word_id]

    # Mapping transcripts to full topic descriptions, for printing (and later saving list, but will probably not be used in frontend)
    transcripts_to_full_topics = {}
    for filename, topic_id in topic_assignments.items():
        description = ", ".join([f"{word} ({prob:.3f})" for word, prob in full_topic_descriptions[topic_id]])
        transcripts_to_full_topics.setdefault(description, []).append(filename)

    # Mapping transcripts to simplified topics, for printing (and later saving list for use in frontend )
    transcripts_to_simplified_topics = {}
    for filename, topic_id in topic_assignments.items():
        simplified_word = simplified_topics[topic_id]
        transcripts_to_simplified_topics.setdefault(simplified_word, []).append(filename)

    # Save the mappings for use in frontend (commented out for testing)
    """
    with open('transcripts_to_full_topics.json', 'w') as f:
        json.dump(transcripts_to_full_topics, f)

    with open('transcripts_to_simplified_topics.json', 'w') as f:
        json.dump(transcripts_to_simplified_topics, f)
    """
    # Printing processed transcripts for testing purposes
    """
    print("\nPrinting processed transcripts for testing purposes:\n")
    for filename, text in zip(file_names, transcripts):
        print(f"{filename}: {text[:100]}") #100 first words only
    """    
    # Print full topic descriptions with associated transcripts
    """
    print("\nPrinting full topic descriptions with associated transcripts for testing purposes:\n")
    for description, filenames in transcripts_to_full_topics.items():
        print(f"Description: {description}")
        for f in filenames:
            print(f" - {f}")
    """
    # Print simplified topics with associated transcripts
    print("\nPrinting simplified topics with associated transcripts for testing purposes:\n")
    for word, filenames in transcripts_to_simplified_topics.items():
        print(f"\nTopic '{word}':")
        for f in filenames:
            print(f" - {f}")

    print("\nTopic assignments and processed transcripts have been saved and/or printed.")
    print('\nCoherence Score:\n ', coherence_lda)
