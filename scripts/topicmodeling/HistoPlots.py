import json
import os
import matplotlib.pyplot as plt

# Step 1: Read the JSON file
json_file_path = 'tfidfwithstopwords/tfidfkmeansstopwordstopicmappings.json'  # Update with your JSON file path
with open(json_file_path, 'r') as file:
    data = json.load(file)

# Extract the directory path and file name from the JSON file path
directory_path, json_file_name = os.path.split(json_file_path)

# Remove the file extension from the JSON file name
json_file_name_without_extension = os.path.splitext(json_file_name)[0]

# Construct the plot file name with "H-" prefix
plot_file_name = f'H-{json_file_name_without_extension}.png'

# Step 2: Count the number of entries for each key
entry_counts = {key: len(value) for key, value in data.items()}

# Step 3: Sort the keys based on the number of entries and select the top 100
top_keys = sorted(entry_counts, key=entry_counts.get, reverse=True)[:100]
top_counts = [entry_counts[key] for key in top_keys]

# Define a single color for all bars
bar_color = 'blue'

# Step 4: Create a histogram
plt.figure(figsize=(10, 6))
plt.bar(top_keys, top_counts, color=bar_color)

# Define the original title size
original_title_size = 20

# Set axis labels with the size that the title was before the change
plt.xlabel('Topic', fontsize=original_title_size)
plt.ylabel('Transcript Frequency', fontsize=original_title_size)

# Set title with increased font size and bold
plt.title('Distribution of Transcripts by Topic', fontsize=original_title_size)

# Remove x-axis category labels
plt.xticks(ticks=[], labels=[])

plt.tight_layout()

# Construct the path for saving the plot in the same directory as the JSON file
plot_save_path = os.path.join(directory_path, plot_file_name)

# Save the plot as a PNG file
plt.savefig(plot_save_path)

plt.close()
