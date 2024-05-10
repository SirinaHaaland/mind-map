import json
from nltk.corpus import wordnet as wn
import nltk
nltk.download('wordnet')

def map_topics_to_main_category(json_file_path):
    with open(json_file_path, 'r') as f:
        topics_data = json.load(f)

    # Map each category to its main category based on hypernym hierarchy
    mapped_topics = {}
    for category, details in topics_data.items():
        main_category = find_main_category(category)
        if main_category not in mapped_topics:
            mapped_topics[main_category] = {}
        mapped_topics[main_category][category] = details

    return mapped_topics

# Function to find main category based on hierarchy
def find_main_category(category):
    # Get synsets for the category
    synsets = wn.synsets(category)

    # Initialize a set to store all related categories
    related_categories = set([category])

    # Traverse the hypernym hierarchy and collect related categories
    for synset in synsets:
        hypernyms = synset.hypernyms()
        for hypernym in hypernyms:
            related_categories.update(get_category_names(hypernym))

    # Find the main category from the related categories
    return min(related_categories, key=len)  # Choose the shortest category name as main category

# Function to get category names from a synset and its hypernyms
def get_category_names(synset):
    names = set(synset.lemma_names())
    for hypernym in synset.hypernyms():
        names.update(get_category_names(hypernym))
    return names

json_file_path = 'MappedTopics.json'
mapped_topics = map_topics_to_main_category(json_file_path)

# Store the mapped topics in a JSON file
output_file_path = 'mapped_topics.json'
with open(output_file_path, 'w') as outfile:
    json.dump(mapped_topics, outfile, indent=4)

print("Mapped topics stored in:", output_file_path)
