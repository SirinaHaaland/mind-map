import os
import re
import json
from transformers import AutoTokenizer, AutoModelForCausalLM

def preprocess_text(text):
    text = re.sub(r'\s+', ' ', text).strip() # removes any irregular spacing (spaces, tabs, newlines, etc.)
    return text

# initialize tokenizer and model from the pretrained GPT-J model from Hugging Face
# the tokenizer is used to convert text to tokens (numerical representations)
tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-j-6B")
model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-j-6B")

directory_path = '..data/transcripts/CleanedTranscripts'
topic_mappings = {}  # map each topic to a list of file names associated with that topic

for file_name in os.listdir(directory_path):
    file_path = os.path.join(directory_path, file_name)
    with open(file_path, 'r', encoding='utf-8') as file:
        transcript_text = file.read()  # Read the entire content of the file into a single string

    preprocessed_text = preprocess_text(transcript_text)
    # sentence = f"Read the following text carefully. Identify and return a single word that represents the primary topic or theme described in the text. The keyword should reflect the essence of the discussion: {preprocessed_text}"
    # sentence = f"Generate one topic word for this text: {preprocessed_text}"
    # sentence = f"Given the text below, identify one key term that captures the main subject matter: {preprocessed_text}"
    # sentence = f"Analyze the following text and extract a single, relevant keyword that best summarizes the overarching theme: {preprocessed_text}"
    sentence = f"Identify the primary topic of the text in one word, similar to how 'technology' might summarize a discussion on smartphones, or 'environment' could describe a passage on climate change: {preprocessed_text}"

    # encoding input text
    inputs = tokenizer(sentence, return_tensors='pt', truncation=True, max_length=1000, padding="max_length")

    # generate the output, adjust max_new_tokens to preferred length of output
    outputs = model.generate(inputs.input_ids, max_length=inputs.input_ids.shape[1] + 1, pad_token_id=tokenizer.eos_token_id, do_sample=True, num_beams=5, no_repeat_ngram_size=2, early_stopping=True)

    # decode only the generated part, skipping the input tokens
    generated_part = outputs[:, inputs.input_ids.shape[1]:]
    topic = tokenizer.decode(generated_part[0], skip_special_tokens=True)

    print(f"Topic for {file_name}: {topic}")
    # append file name to the list of files for the generated topic word
    if topic not in topic_mappings:
            topic_mappings[topic] = []
    topic_mappings[topic].append(file_name)

# export mappings to a JSON file
with open('gptj_topic_mappings.json', 'w', encoding='utf-8') as f:
    json.dump(topic_mappings, f, ensure_ascii=False, indent=4)


