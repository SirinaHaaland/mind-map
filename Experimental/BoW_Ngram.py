import os
import nltk
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer


nltk.download('punkt')


def read_preprocessed_files(directory):
    preprocessed_files = {}
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                preprocessed_content = file.read()
                preprocessed_files[filename[:-4]] = preprocessed_content
    return preprocessed_files

def generate_ngrams(text, n=2):
    tokens = word_tokenize(text)
    ngrams = []
    for i in range(len(tokens) - n + 1):
        ngram = ' '.join(tokens[i:i + n])
        ngrams.append(ngram)
    return ngrams


def create_bow_representation(text):
    vectorizer = CountVectorizer()
    bow_matrix = vectorizer.fit_transform([text])
    return bow_matrix, vectorizer

def main():

    directory = 'preprocessed_files'
    output_directory = 'ngram_bow_files'
    os.makedirs(output_directory, exist_ok=True)
    preprocessed_files = read_preprocessed_files(directory)

    if not preprocessed_files:
        print("No preprocessed text files found in the directory.")
        return


    for transcript_name, preprocessed_text in preprocessed_files.items():

        bigrams = generate_ngrams(preprocessed_text, n=2)
        trigrams = generate_ngrams(preprocessed_text, n=3)
        bow_matrix, vectorizer = create_bow_representation(preprocessed_text)


        with open(os.path.join(output_directory, f'{transcript_name}_bigrams.txt'), 'w', encoding='utf-8') as file:
            file.write('\n'.join(bigrams))
        with open(os.path.join(output_directory, f'{transcript_name}_trigrams.txt'), 'w', encoding='utf-8') as file:
            file.write('\n'.join(trigrams))
        with open(os.path.join(output_directory, f'{transcript_name}_bow_matrix.txt'), 'w', encoding='utf-8') as file:
            file.write(str(bow_matrix))

    print("N-grams and bag-of-words representations saved successfully.")

if __name__ == "__main__":
    main()
