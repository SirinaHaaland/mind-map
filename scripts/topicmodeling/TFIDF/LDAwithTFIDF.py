"""
TF-IDF can help emphasize words that are unique to certain documents, potentially 
improving the quality of your topics by reducing the impact of frequently occurring 
words that are less informative about the document's specific content.
We can still include a stopwords list, lemmatization, and bigrams/trigrams.
"""
import os
import re
import json
from gensim import corpora
import gensim
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from gensim.models.coherencemodel import CoherenceModel
from gensim.models import TfidfModel
from gensim.models.phrases import Phrases, Phraser

def preprocess(text):
    lines = text.split('\n')
    processed_lines = []
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    
    for line in lines:
        # Further processing (removing non-alphabetic characters, tokenizing, etc.)
        line = re.sub('[^A-Za-z]+', ' ', line)
        tokens = word_tokenize(line.lower())
        processed_tokens = [lemmatizer.lemmatize(w) for w in tokens if w not in stop_words]
        processed_lines.extend(processed_tokens)
    
    return processed_lines

def load_and_preprocess_transcripts(directory):
    transcripts = []
    file_names = []
    for filename in os.listdir(directory):
        if filename.endswith('.stm'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                processed_text = preprocess(text)
                transcripts.append(processed_text)
                file_names.append(filename)
    return transcripts, file_names

if __name__ == '__main__':
    # Load and preprocess transcripts
    directory = '../../../data/transcripts/CleanedTranscripts'
    transcripts, file_names = load_and_preprocess_transcripts(directory)

    bigram = Phrases(transcripts, min_count=5, threshold=100) # Higher threshold fewer phrases.
    trigram = Phrases(bigram[transcripts], threshold=100) # Depending on your preference, you can skip trigram

    # Turn the Phrases model into a Phraser object for faster performance
    bigram_phraser = Phraser(bigram)
    trigram_phraser = Phraser(trigram)

    transcripts = [trigram_phraser[bigram_phraser[doc]] for doc in transcripts]

    # Create the Dictionary and Corpus
    dictionary = corpora.Dictionary(transcripts)
    corpus = [dictionary.doc2bow(text) for text in transcripts]

    tfidf = TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]

    # Apply LDA, try out different numbers of topics and passes
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=230, id2word=dictionary, passes=15)

    # Coherence Model for evaluating topic quality
    coherence_model_lda = CoherenceModel(model=ldamodel, texts=transcripts, dictionary=dictionary, coherence='c_v')
    coherence_lda = coherence_model_lda.get_coherence()
    print('\nCoherence Score:\n ', coherence_lda) #Between 0 and 1, over 0.5 considered good

    topic_assignments = {}
    for i in range(len(file_names)):
    # Get the list of topic probabilities for the i-th document
        topic_probs = ldamodel.get_document_topics(corpus[i], minimum_probability=0)
        topic_assignments[file_names[i]] = max(topic_probs, key=lambda x: x[1])[0]

    # Generate full topic descriptions (to print/see the words in each topic, not just topic id))
    full_topic_descriptions = {i: ldamodel.show_topic(i) for i in range(ldamodel.num_topics)}

    # Simplify/reduce topics to one (the most significant) word
    simplified_topics = {}
    for topic_id in range(ldamodel.num_topics):
        word_id, _ = max(ldamodel.get_topic_terms(topic_id), key=lambda x: x[1])
        simplified_topics[topic_id] = ldamodel.id2word[word_id]

    # Mapping transcripts to simplified topics, for printing (and later saving list for use in frontend )
    transcripts_to_simplified_topics = {}
    for filename, topic_id in topic_assignments.items():
        simplified_word = simplified_topics[topic_id]
        transcripts_to_simplified_topics.setdefault(simplified_word, []).append(filename)

# Saving simplified topic assignments to a JSON file
    with open('lda_with_tfidf_topic_mappings.json', 'w', encoding='utf-8') as f:
        json.dump(transcripts_to_simplified_topics, f, ensure_ascii=False, indent=4)

    for word, filenames in transcripts_to_simplified_topics.items():
        print(f"Topic '{word}':")
        for f in filenames:
            print(f" - {f}")

    print('\nCoherence Score:\n ', coherence_lda)
