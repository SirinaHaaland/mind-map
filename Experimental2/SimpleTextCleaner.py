import os
import re

def clean_text(text):
    # Remove <NA> and everything before it, then remove <unk>
    cleaned_text = re.sub(r'.*<NA>\s?', '', text)
    cleaned_text = re.sub('<unk>', '', cleaned_text)
    return cleaned_text

def save_clean_transcripts(input_directory, output_directory):
    for filename in os.listdir(input_directory):
        if filename.endswith('.stm'):
            input_file_path = os.path.join(input_directory, filename)
            with open(input_file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                cleaned_text = clean_text(text)
            
            # Construct path for the cleaned transcript
            output_file_path = os.path.join(output_directory, filename)
            # Save cleaned transcript
            with open(output_file_path, 'w', encoding='utf-8') as file:
                file.write(cleaned_text)

if __name__ == '__main__':
    input_directory = r'../Experimental2/UnProcessTranscripts'
    output_directory = r'../Experimental2/TestTranscripts'
    save_clean_transcripts(input_directory, output_directory)
