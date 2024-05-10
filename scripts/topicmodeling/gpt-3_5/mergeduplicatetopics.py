import json

def merge_json_duplicates(file_path):
    # Read the original JSON data from the provided file path
    with open('gpt-3_5topicmappings.json', 'r') as file:
        json_data = json.load(file)

    # Temporary storage to track which keys have been added (case-insensitive)
    seen_keys = {}
    # The final merged JSON data
    merged_data = {}

    for key, value in json_data.items():
        # Determine if the key (in lowercase) has been seen
        lower_key = key.lower()
        if lower_key in seen_keys:
            # If seen, append the value to the existing key's list
            merged_data[seen_keys[lower_key]].extend(value)
        else:
            # If not seen, add the key and value as is, and mark it as seen
            merged_data[key] = value
            seen_keys[lower_key] = key

    # Save the merged data back to a new JSON file
    with open('mergedgpt-3_5topicmappings.json', 'w') as outfile:
        json.dump(merged_data, outfile, indent=4)

# The path to the original JSON file - adjust as necessary for the actual file location
file_path = 'gpt-3_5topicmappings.json'

# Call the function to merge duplicates and save to a new file
merge_json_duplicates(file_path)
