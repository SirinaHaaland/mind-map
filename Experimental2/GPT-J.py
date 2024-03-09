"""
#Testcode for checking if the model can be loaded on unix system
#(did not load locally, probably not enough memory)

from transformers import AutoTokenizer, AutoModelForCausalLM

try:
    print("Attempting to load model and tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-j-6B")
    model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-j-6B")
    print("Model and tokenizer loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
"""
import torch
import os
import re
import os
from transformers import AutoTokenizer, AutoModelForCausalLM

def preprocess_text(text):
    # Simplify whitespace to a single space
    text = re.sub(r'\s+', ' ', text).strip()
    return text

#initialize tokenizer and model from pretrained GPT-J (gpt3) model from Huggingface
tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-j-6B")
model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-j-6B")

directory_path = 'C:/Users/sirin/DATBAC-1/STG0006948/Experimental2/TestTranscripts'
for file_name in os.listdir(directory_path):
    file_path = os.path.join(directory_path, file_name)
    transcript_text = open(file_path, 'r', encoding='utf-8').read()

    preprocessed_text = preprocess_text(transcript_text)

    #sentence = "Generate one topic word for this text: The giraffe is a large African hoofed mammal belonging to the genus Giraffa. It is the tallest living terrestrial animal and the largest ruminant on Earth. Traditionally, giraffes have been thought of as one species, Giraffa camelopardalis, with nine subspecies. Most recently, researchers proposed dividing them into up to eight extant species due to new research into their mitochondrial and nuclear DNA, as well as morphological measurements. Seven other extinct species of Giraffa are known from the fossil record."
    #sentence = "What is AI?"
    sentence = f"Generate one topic word for this text: {transcript_text}"

    #encoding sentence for model to process
    inputs = tokenizer.encode(sentence, return_tensors='pt', max_length=1000, truncation=True)

    #generating texts, change max_new_tokens to preferred length of answer from gpt2
    outputs = model.generate(inputs, max_new_tokens=5, do_sample=True, num_beams=5, no_repeat_ngram_size=2, early_stopping=True)

    # Calculate the number of tokens in the input sentence
    num_input_tokens = len(inputs[0])
    # Decode only the generated part, skipping the input tokens
    generated_part = outputs[0][num_input_tokens:]
    text = tokenizer.decode(generated_part, skip_special_tokens=True)

    #decoding texts
    #text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    print("Printing generated answer from GPT-J:")
    print(text)

    break #just remove break to run through all files, now it only runs through the first file
