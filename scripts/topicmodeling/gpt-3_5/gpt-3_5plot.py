import json
import plotly.graph_objects as go

# Load the topic mappings from the JSON file
with open('mergedgpt-3_5topicmappings.json', 'r', encoding='utf-8') as f:
    topic_mappings = json.load(f)

# Sort topics by the number of files, in descending order
sorted_topics = sorted(topic_mappings.items(), key=lambda item: len(item[1]), reverse=True)
# Create a list of strings, each containing the topic and the count of files
topics_list = [f'{idx + 1}. {topic.strip()}: {len(files)}' for idx, (topic, files) in enumerate(sorted_topics)]

# Construct the text for the plot
full_text = "<br>".join(topics_list)

# Calculate the number of lines in the text
num_lines = len(topics_list)

# Set the line height (in pixels)
line_height = 20  # Adjust as needed

# Calculate the total height of the text (in pixels)
total_height_px = num_lines * line_height

# Calculate the maximum line width
max_line_width = max(len(line) for line in topics_list)

# Calculate the plot width dynamically based on the maximum line width
# You can adjust the scaling factor (e.g., 10) to control the plot width
plot_width_px = max_line_width * 10  # Adjust scaling factor as needed

# Create a Plotly figure with a single trace containing the text
fig = go.Figure(go.Scatter(
    x=[0],
    y=[0],
    mode="text",
    text=[full_text],
    textfont=dict(family="Courier New", size=12),
    showlegend=False
))

# Update layout to align text to the left and set figure size
fig.update_layout(
    xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
    yaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
    width=plot_width_px,  # Set figure width dynamically
    height=total_height_px,  # Set figure height dynamically
    margin=dict(l=20, r=20, t=20, b=20),  # Add margins to avoid clipping text
    autosize=False  # Disable autosizing to ensure the specified width and height are respected
)

# Save the plot as a PNG file
output_path = 'GPT-3_5plot.png'
fig.write_image(output_path)

print(f"Plot saved as PNG: {output_path}")
