import os
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def read_stm_files(directory):
    stm_files = []
    for filename in os.listdir(directory):
        if filename.endswith('.stm'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                stm_content = file.read()
                stm_files.append((filename, stm_content)) 
    return stm_files

def preprocess_text(text):
    text = text.translate(str.maketrans('', '', string.punctuation))

    tokens = word_tokenize(text)
    
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
    
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]
    
    preprocessed_text = ' '.join(lemmatized_tokens)
    
    return preprocessed_text

def main():
    input_directory = 'cleaned_transcripts'
    
    output_directory = 'preprocessed_files'
    os.makedirs(output_directory, exist_ok=True)

    stm_transcripts = read_stm_files(input_directory)

    if not stm_transcripts:
        print("No STM files found in the directory.")
        return

    for filename, transcript in stm_transcripts:
        preprocessed_text = preprocess_text(transcript)
        output_file_path = os.path.join(output_directory, filename.replace('.stm', '_preprocessed.txt'))
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(preprocessed_text)
    
    print("Preprocessing completed. Preprocessed files saved in the output directory.")

if __name__ == "__main__":
    main()
