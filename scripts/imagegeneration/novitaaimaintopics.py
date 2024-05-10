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
json_file_path = "selectedtopics.json"  

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

# Generate one image for each category
for category, filenames in normalized_categories:
    # Generate image for the current category
    res = client.txt2img_v3(
        model_name='protovisionXLHighFidelity3D_release0630Bakedvae_154359.safetensors',
        prompt=category,
        width=512,
        height=512,
        image_num=1,
        guidance_scale=7.5,
        seed=12345,
        sampler_name=Samplers.EULER_A
    )

    # Create the output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)

    # Save the generated image with the appropriate filename in the output directory
    base64_to_image(res.images_encoded[0]).save(os.path.join(output_path, f"{category}_M.png"))

print("Image generation complete.")
