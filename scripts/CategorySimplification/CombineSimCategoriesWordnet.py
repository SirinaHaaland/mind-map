import json
from nltk.corpus import wordnet as wn
import nltk
from collections import defaultdict
nltk.download('wordnet')

def map_topics_to_main_category(json_file_path):
    with open(json_file_path, 'r') as f:
        topics_data = json.load(f)

    # Map each category to its main category based on synonyms
    mapped_topics = {}
    grouped_categories = set()

    # Create a defaultdict to store categories grouped by synonyms
    synonyms_groups = defaultdict(set)

    for category, details in topics_data.items():
        synonyms = get_synonyms(category)
        synonyms_groups[frozenset(synonyms)].add(category)

    for synonyms_set, categories_set in synonyms_groups.items():
        main_category = max(categories_set, key=lambda x: len(get_synonyms(x)))
        if len(categories_set) > 1:
            mapped_topics[main_category] = {c: topics_data[c] for c in categories_set}
            grouped_categories.update(categories_set)
        else:
            mapped_topics.update({c: details for c in categories_set})  # Add single categories as they are

    # Sort mapped topics by category name
    mapped_topics = dict(sorted(mapped_topics.items()))

    return mapped_topics

# Function to get synonyms for a category using WordNet
def get_synonyms(category):
    synonyms = set()
    synsets = wn.synsets(category)
    for synset in synsets:
        for lemma in synset.lemmas():
            synonyms.add(lemma.name())
    return synonyms

json_file_path = 'MappedTopics.json'
mapped_topics = map_topics_to_main_category(json_file_path)

# Store the mapped topics in a JSON file
output_file_path_mapped = 'mapped_topics.json'
with open(output_file_path_mapped, 'w') as outfile:
    json.dump(mapped_topics, outfile, indent=4)

print("Mapped topics stored in:", output_file_path_mapped)
