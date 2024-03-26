import os
import re
import json
from gensim import corpora
import gensim
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from gensim.models.coherencemodel import CoherenceModel
from gensim.models import Phrases
from gensim.models.phrases import Phraser

def minimal_preprocess(text):
    # Basic cleaning and tokenization for phrase detection
    cleaned_text = re.sub(r'.*<NA>\s?', '', text)
    cleaned_text = re.sub('<unk>', ' ', cleaned_text)
    cleaned_text = re.sub(r'\b\w{1,2}\b', '', cleaned_text)
    cleaned_text = re.sub('[^A-Za-z]+', ' ', cleaned_text)
    tokens = word_tokenize(cleaned_text.lower())
    return tokens

def train_phrases(transcripts):
    # train the Phrases model to detect common phrases (bigrams or more)
    phrases = Phrases(transcripts, min_count=5, threshold=10)
    bigram = Phraser(phrases)
    return bigram

def preprocess(tokens, bigram_model):
    # Apply the Phrases model to merge detected phrases into single tokens
    tokens_with_phrases = bigram_model[tokens]
    # Continue with your preprocessing (stopwords removal, lemmatization, etc.)
    stop_words = set(stopwords.words('english'))
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
    directory = '../../../data/transcripts/CleanedTranscripts'
    transcripts, file_names = load_and_preprocess_transcripts(directory)

    dictionary = corpora.Dictionary(transcripts) #Creates a Gensim dictionary from the transcripts. This dictionary maps each unique token (word) in the transcripts to a unique integer ID. Necessary for converting the transcripts into a numerical format that can be used for LDA analysis.
    corpus = [dictionary.doc2bow(text) for text in transcripts] #Converts each transcript into the Bag-of-Words (BoW) format using the previously created dictionary. The BoW model represents each document as a vector of token frequencies, ignoring the order of words but maintaining the information about word occurrences. doc2bow converts the transcript into a sparse representation of the token IDs and their frequencies in the document.

    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=3000, id2word=dictionary, passes=15) #Initializes and trains the LDA model on the corpus. This model will try to find 300 topics in the corpus. The id2word parameter is the dictionary that maps IDs to tokens, necessary for interpreting the topics. The passes parameter defines how many times the model iterates over the entire corpus during training, with more passes potentially leading to a better model at the cost of longer training time.

    coherence_model_lda = CoherenceModel(model=ldamodel, texts=transcripts, dictionary=dictionary, coherence='c_v') #Initializes a Coherence Model using the trained LDA model, the preprocessed transcripts, and the Gensim dictionary. The coherence measure used is 'c_v', a popular choice for evaluating topic models. This measure assesses the coherence of the topics identified by the model, essentially estimating how meaningful the topics are by examining the degree of semantic similarity between high scoring words within each topic.
    coherence_lda = coherence_model_lda.get_coherence() #Calculates the coherence score of the LDA model based on the 'c_v' measure. A higher coherence score indicates that the topics are more interpretable and meaningful, suggesting that the model does a good job of capturing the thematic structure of the corpus.
    print('\nCoherence Score:\n ', coherence_lda) 

    # Extracting the most significant topic for each transcript and assigning that topic to the transcript 
    topic_assignments = {file_names[i]: max(ldamodel[corpus[i]], key=lambda x: x[1])[0] for i in range(len(file_names))}

    # Generate full topic descriptions (to print/see the words in each topic, not just topic id))
    full_topic_descriptions = {i: ldamodel.show_topic(i) for i in range(ldamodel.num_topics)}

    # Simplify/reduce topics to one (the most significant) word
    simplified_topics = {}
    for topic_id in range(ldamodel.num_topics):
        word_id, _ = max(ldamodel.get_topic_terms(topic_id), key=lambda x: x[1])
        simplified_topics[topic_id] = ldamodel.id2word[word_id]

    # Mapping transcripts to simplified topics 
    transcripts_to_simplified_topics = {}
    for filename, topic_id in topic_assignments.items():
        simplified_word = simplified_topics[topic_id]
        transcripts_to_simplified_topics.setdefault(simplified_word, []).append(filename)

    output_file_path = 'LDAforIMAGEgen_topic_mappings.json'  
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(transcripts_to_simplified_topics, f, ensure_ascii=False, indent=4)

    # Print simplified topics with associated transcripts
    for word, filenames in transcripts_to_simplified_topics.items():
        print(f"\nTopic '{word}':")
        for f in filenames:
            print(f" - {f}")

    print('\nCoherence Score:\n ', coherence_lda)