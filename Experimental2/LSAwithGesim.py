import os
import re
import json
from gensim import corpora, models
import gensim
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from gensim.models.coherencemodel import CoherenceModel
from gensim.models import Phrases
from gensim.models.phrases import Phraser

# Assuming NLTK data has been downloaded as per the commented-out section
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
    stop_words = set(stopwords.words('english'))
    stop_words.update({'said', 'thing', 'like', 'could', 'one', 'get', 'people', 
    'would', 'going', 'make', 'think', 'know', 'team', 'see', 'way', 'say', 'really', 
    'actually', 'world', 'way', 'life', 'thing', 'well', 'also', 'story', 'life', 
    'time', 'thing'})
    lemmatizer = WordNetLemmatizer()
    processed_tokens = [lemmatizer.lemmatize(w) for w in tokens_with_phrases if w not in stop_words]
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
    directory = '../data/TEDLIUM_release-3/TEDLIUM_release-3/data/stm'
    transcripts, file_names = load_and_preprocess_transcripts(directory)

    dictionary = corpora.Dictionary(transcripts)
    corpus = [dictionary.doc2bow(text) for text in transcripts]

    # Train the LSI Model
    lsamodel = gensim.models.LsiModel(corpus, num_topics=200, id2word=dictionary)

    # Evaluate the model
    coherence_model_lsi = CoherenceModel(model=lsamodel, texts=transcripts, dictionary=dictionary, coherence='c_v')
    coherence_lsi = coherence_model_lsi.get_coherence()
    print('\nCoherence Score: ', coherence_lsi)

    # Extracting the most significant topic for each transcript and assigning that topic to the transcript
    topic_assignments = {file_names[i]: max(lsamodel[corpus[i]], key=lambda x: abs(x[1]))[0] for i in range(len(file_names))}

    # Generate full topic descriptions
    full_topic_descriptions = {i: lsamodel.show_topic(i) for i in range(lsamodel.num_topics)}

    # Simplify/reduce topics to one (the most significant) word
# Simplify/reduce topics to one (the most significant) word
    simplified_topics = {}
    for topic_id in range(lsamodel.num_topics):
    # Using show_topic to get the list of tuples for each topic
        topic_terms = lsamodel.show_topic(topic_id, topn=1)  # Get only the top term
        if topic_terms:  # Ensure the list is not empty
            word, _ = topic_terms[0]  # Get the word from the first tuple
            simplified_topics[topic_id] = word

    # Mapping transcripts to simplified topics, for printing
    transcripts_to_simplified_topics = {}
    for filename, topic_id in topic_assignments.items():
        simplified_word = simplified_topics[topic_id]
        transcripts_to_simplified_topics.setdefault(simplified_word, []).append(filename)

    # Printing simplified topics with associated transcripts for testing purposes
    print("\nPrinting simplified topics with associated transcripts for testing purposes:\n")
    for word, filenames in transcripts_to_simplified_topics.items():
        print(f"Topic '{word}':")
        for f in filenames:
            print(f" - {f}")

    print("\nTopic assignments and processed transcripts have been saved and/or printed.")
    print('\nCoherence Score: ', coherence_lsi)
