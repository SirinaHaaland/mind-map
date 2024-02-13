import os
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Function to read STM files from a directory
def read_stm_files(directory):
    stm_files = []
    for filename in os.listdir(directory):
        if filename.endswith('.stm'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                stm_content = file.read()
                stm_files.append((filename, stm_content))  # Keep filename along with content
    return stm_files

# Function for text preprocessing
def preprocess_text(text):
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Tokenize the text
    tokens = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
    
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]
    
    # Join the tokens back into a single string
    preprocessed_text = ' '.join(lemmatized_tokens)
    
    return preprocessed_text

# Main function
def main():
    # Directory containing STM files
    input_directory = 'cleaned_transcripts'
    
    # Output directory for preprocessed files
    output_directory = 'preprocessed_files'
    os.makedirs(output_directory, exist_ok=True)

    # Read all STM files from the input directory
    stm_transcripts = read_stm_files(input_directory)

    if not stm_transcripts:
        print("No STM files found in the directory.")
        return

    # Preprocess each transcript and write to output directory
    for filename, transcript in stm_transcripts:
        preprocessed_text = preprocess_text(transcript)
        output_file_path = os.path.join(output_directory, filename.replace('.stm', '_preprocessed.txt'))
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(preprocessed_text)
    
    print("Preprocessing completed. Preprocessed files saved in the output directory.")

if __name__ == "__main__":
    main()
