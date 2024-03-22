import json
import matplotlib.pyplot as plt

# load the topic mappings from the JSON file
with open('C:/Users/sirin/DATBAC-1/STG0006948/scripts/topicmodeling/IDF/idf_kmeans_topic_mappings.json', 'r', encoding='utf-8') as f:
    topic_mappings = json.load(f)

# Sort topics by the number of files, in descending order
sorted_topics = sorted(topic_mappings.items(), key=lambda item: len(item[1]), reverse=True)
# create a list of strings, each containing the topic and the count of files
topics_list = [f'{idx + 1}. {topic.strip()}: {len(files)}' for idx, (topic, files) in enumerate(sorted_topics)]

def create_topic_image(topics_list, output_path):
    modelname = "IDF with Kmeans Topic Model\n"
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
output_path = 'C:/Users/sirin/DATBAC-1/STG0006948/scripts/topicmodeling/IDF/IDF_Kmeans_plot.png'
create_topic_image(topics_list, output_path)

"""
The JSON structure in the topic modeling script should map each topic word 
to a list of file names associated with that topic.
For example, gpt2_topic_mappings.json should look like this:
{
    "friendship": [
        "transcript1.txt",
        "transcript3.txt"
    ],
    "tragedy": [
        "transcript2.txt",
        "transcript4.txt"
    ]
}
"""