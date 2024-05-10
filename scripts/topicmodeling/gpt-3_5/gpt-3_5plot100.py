# Plots the first 100 generated topics only for brievity

import json
import matplotlib.pyplot as plt

# Load the topic mappings from the JSON file
with open('gpt-3_5topicmappings.json', 'r', encoding='utf-8') as f:
    topic_mappings = json.load(f)

# Sort topics by the number of files, in descending order
sorted_topics = sorted(topic_mappings.items(), key=lambda item: len(item[1]), reverse=True)

# Create a list of strings, each containing the topic and the count of files for the first 100 topics
topics_list = [f'{idx + 1}. {topic.strip()}: {len(files)}' for idx, (topic, files) in enumerate(sorted_topics[:100])]

def create_topic_image(topics_list, output_path):
    modelname = "GPT-3.5 Topic Model\n"
    header = "Nr. Topic: Count"
    full_text = modelname + "\n" + header + "\n" + "\n".join(topics_list)
    # Adjust figure height based on the number of topics
    plt.figure(figsize=(10, max(0.5 * len(topics_list), 10)))
    # Place text at the top left, adjusting the vertical alignment
    plt.text(0, 1, full_text, ha='left', va='top', fontsize=12, family='monospace')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight')

# Specify the output path for the generated image
output_path = 'GPT-3_5plot100.png'
create_topic_image(topics_list, output_path)
