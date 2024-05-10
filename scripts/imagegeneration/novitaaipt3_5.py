import json
import os
from novita_client import NovitaClient, Samplers
from novita_client.utils import base64_to_image

# Define your Novita API key and endpoint
novita_api_key = "your novita api key goes here"
novita_api_endpoint = "https://api.novita.ai"

# Set the Novita API key as an environment variable
os.environ["NOVITA_API_KEY"] = novita_api_key

# Initialize Novita client
client = NovitaClient(novita_api_key, novita_api_endpoint)

# Path to the JSON file containing category mappings
json_file_path = "mergedgpt35topicmappings.json"  

# Output directory path for saving generated images
output_path = "../../data/images"  

# Load category mappings from JSON file
with open(json_file_path, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Normalize categories (remove duplicates and convert to lowercase)
categories_set = set()
normalized_categories = []
for category, filenames in data.items():
    category_lower = category.lower()
    if category_lower not in categories_set:
        categories_set.add(category_lower)
        normalized_categories.append((category, filenames))

# Function to split a list into chunks of size n
def chunk_list(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

# Generate images for each category
for category, filenames in normalized_categories:
    # Count the number of elements in the category
    num_elements = len(filenames)
    
    # Calculate the number of images to generate
    num_images = num_elements # Generates images for the image for the audio files

    # Split the number of images into chunks of 8 (max allowed by the API)
    chunks = list(chunk_list(range(num_images), 8))

    # Generate images for each chunk
    for chunk_idx, chunk in enumerate(chunks):
        # Generate images for the current chunk
        res = client.txt2img_v3(
            model_name='protovisionXLHighFidelity3D_release0630Bakedvae_154359.safetensors',
            prompt=category,  # Prompt with the category name for the extra image
            width=512,
            height=512,
            image_num=len(chunk),  # Number of images to generate in this chunk
            guidance_scale=7.5,
            seed=12345,
            sampler_name=Samplers.EULER_A
        )
        
        # Create the output directory if it doesn't exist
        os.makedirs(output_path, exist_ok=True)

        # Save the generated images with the appropriate filenames in the output directory
        for i, filename_idx in enumerate(chunk):
            if filename_idx < num_elements:
                filename = filenames[filename_idx]
                base64_to_image(res.images_encoded[i]).save(os.path.join(output_path, f"{category}_{filename}.png"))
            else:
                base64_to_image(res.images_encoded[i]).save(os.path.join(output_path, f"{category}.png"))

print("Image generation complete.")
