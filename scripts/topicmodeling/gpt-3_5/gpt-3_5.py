from openai import OpenAI
import os
import re
import json

# Set your OpenAI API key here
api_key = 'your_api_key' 

# removes any irregular spacing (spaces, tabs, newlines, etc.)
def preprocess_text(text):
    text = re.sub(r'\s+', ' ', text).strip() 
    return text

directory_path = '../../../data/transcripts/cleanedtranscripts'
topic_mappings = {}  # Map each topic to a list of file names associated with that topic

for file_name in os.listdir(directory_path):
    file_path = os.path.join(directory_path, file_name)
    with open(file_path, 'r', encoding='utf-8') as file:
        transcript_text = file.read()  # Read the entire content of the file into a single string

    preprocessed_text = preprocess_text(transcript_text)
    
    client = OpenAI(api_key=api_key)

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
           {"role": "user", "content": f"Identify the primary topic of the text in one word, similar to how 'technology' might summarize a discussion on smartphones, or 'environment' could describe a passage on climate change: {preprocessed_text}"}]
        )
    topic_message = completion.choices[0].message
    topic = topic_message.content  # Extracting the content string from the ChatCompletionMessage

    print(f"Topic for {file_name}: {topic}")
    
    # Append file name to the list of files for the generated topic word
    if topic not in topic_mappings:
        topic_mappings[topic] = []
    topic_mappings[topic].append(file_name)


# Export mappings to a JSON file
with open('gpt-3_5topicmappings.json', 'w', encoding='utf-8') as f:
    json.dump(topic_mappings, f, ensure_ascii=False, indent=4)
