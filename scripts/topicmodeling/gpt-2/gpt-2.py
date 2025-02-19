import os  
import re 
import json
from transformers import GPT2LMHeadModel, GPT2Tokenizer

def preprocess_text(text): 
    cleaned_text = re.sub(r'\s+', ' ', text).strip() # removes any irregular spacing (spaces, tabs, newlines, etc.)
    return cleaned_text

# Initialize tokenizer and pre-trained GPT-2 model from Hugging Face's Transformers library
# Ihe tokenizer is used to convert text to tokens (numerical representations)
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2', pad_token_id=tokenizer.eos_token_id)

directory_path = '../../../data/transcripts/cleanedtranscripts'
topic_mappings = {}  # Map each topic to a list of file names associated with that topic
for file_name in os.listdir(directory_path):
    file_path = os.path.join(directory_path, file_name)
    with open(file_path, 'r', encoding='utf-8') as file:
        transcript_text = file.read() # Reads the entire content of the file into a single string


    preprocessed_text = preprocess_text(transcript_text)
    # sentence = f"Read the following text carefully. Identify and return a single word that represents the primary topic or theme described in the text. The keyword should reflect the essence of the discussion: {preprocessed_text}"
    # sentence = f"Generate one topic word for this text: {preprocessed_text}"
    # sentence = f"Given the text below, identify one key term that captures the main subject matter: {preprocessed_text}"
    # sentence = f"Analyze the following text and extract a single, relevant keyword that best summarizes the overarching theme: {preprocessed_text}"
    sentence = f"Identify the primary topic of the text in one word, similar to how 'technology' might summarize a discussion on smartphones, or 'environment' could describe a passage on climate change: {preprocessed_text}"
    # encoding input text
    inputs = tokenizer.encode(sentence, return_tensors='pt', max_length=1000, truncation=True)

    # Generate the output, change max_new_tokens to preferred length of output
    outputs = model.generate(inputs, max_new_tokens=1, do_sample=True, num_beams=5, no_repeat_ngram_size=2, early_stopping=True)

    # Calculate the number of tokens in the input sentence
    num_input_tokens = len(inputs[0])
    # Decode only the generated part, skipping the input tokens
    generated_part = outputs[0][num_input_tokens:]
    topic = tokenizer.decode(generated_part, skip_special_tokens=True)

    print(f"Topic for {file_name}: {topic}")
    # Append file name to the list of files for the generated topic word
    if topic not in topic_mappings:
            topic_mappings[topic] = []
    topic_mappings[topic].append(file_name)

    # Export mappings to a JSON file
with open('gpt-2topicmappings.json', 'w', encoding='utf-8') as f:
    json.dump(topic_mappings, f, ensure_ascii=False, indent=4)