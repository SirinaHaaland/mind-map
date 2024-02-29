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

# Ensure you have downloaded the necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def preprocess(text):
    # Split text into lines and process each line to remove unwanted content
    lines = text.split('\n')
    processed_lines = []
    for line in lines:
        # Remove content before <NA> and <NA> itself
        cleaned_line = re.sub(r'.*<NA>\s?', '', line)
        # Further processing (removing non-alphabetic characters, tokenizing, etc.)
        cleaned_line = re.sub(r'\b\w{1,3}\b', '', cleaned_line)
        cleaned_line = re.sub('[^A-Za-z]+', ' ', cleaned_line)
        tokens = word_tokenize(cleaned_line.lower())
        stop_words = set(stopwords.words('english'))
        lemmatizer = WordNetLemmatizer()
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

# Load and preprocess transcripts
directory = '../data/TEDLIUM_release-3/TEDLIUM_release-3/legacy/test/stm'
#directory = '../data/TEDLIUM_release-3/TEDLIUM_release-3/data/stm'
transcripts, file_names = load_and_preprocess_transcripts(directory)

# Create the Dictionary and Corpus
dictionary = corpora.Dictionary(transcripts)
corpus = [dictionary.doc2bow(text) for text in transcripts]

# Save processed transcripts for future use (commented out for testing)
"""
processed_transcripts = {'filename': text for filename, text in zip(file_names, transcripts)}
with open('processed_transcripts.json', 'w') as f:
    json.dump(processed_transcripts, f)
"""

# Apply LDA, try out different numbers of topics and passes
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=4, id2word=dictionary, passes=15)

# Coherence Model for evaluating topic quality
coherence_model_lda = CoherenceModel(model=ldamodel, texts=transcripts, dictionary=dictionary, coherence='c_v')
coherence_lda = coherence_model_lda.get_coherence()
print('\nCoherence Score: ', coherence_lda) #Between 0 and 1, over 0.5 considered good

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
print("Printing processed transcripts for testing purposes:")
for filename, text in zip(file_names, transcripts):
    print(f"{filename}: {text[:100]}") #100 first words only

# Print full topic descriptions with associated transcripts
print("Printing full topic descriptions with associated transcripts for testing purposes:")
for description, filenames in transcripts_to_full_topics.items():
    print(f"Description: {description}")
    for f in filenames:
        print(f" - {f}")

# Print simplified topics with associated transcripts
print("Printing simplified topics with associated transcripts for testing purposes:")
for word, filenames in transcripts_to_simplified_topics.items():
    print(f"Topic '{word}':")
    for f in filenames:
        print(f" - {f}")

#print("Topic assignments and processed transcripts have been saved.")
print("Topic assignments and processed transcripts have been printed.")
print('\nCoherence Score: ', coherence_lda)
#Run script in dir Experimental2 with command: python LDAwithGesim.py
