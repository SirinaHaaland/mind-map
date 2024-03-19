import os
import re
from tqdm import tqdm

def preprocess_text(text):
    return text.lower()

def load_stm_files(folder_path):
    stm_files = []
    file_names = []
    for filename in tqdm(os.listdir(folder_path), desc="Loading STM Files", unit="file"):
        if filename.endswith(".stm"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                stm_files.append(preprocess_text(file.read()))
                file_names.append(filename)
    return stm_files, file_names

def clean_and_save_files(input_folder_path, output_folder_path):
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    stm_files, file_names = load_stm_files(input_folder_path)

    for content, filename in zip(stm_files, file_names):
        content = re.sub(r'.*<o,f0,male>', '', content, flags=re.IGNORECASE)
        content = re.sub(r'.*<o,f0,female>', '', content, flags=re.IGNORECASE)
        content = re.sub(r'.*<o,,unknown>', '', content, flags=re.IGNORECASE)
        content = content.replace("o,f0,male", "").replace("<o,f0,female>", "").replace("<o,,unknown>", "").replace("ignore_time_segment_in_scoring", "").replace("<unk>", "")

        output_file_path = os.path.join(output_folder_path, filename)
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(content)

def main():
    input_folder_path = "Devtranscripts"
    output_folder_path = "cleaned_Devtranscripts"

    clean_and_save_files(input_folder_path, output_folder_path)

if __name__ == "__main__":
    main()
