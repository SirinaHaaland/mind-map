from flask import Flask, request, send_file, send_from_directory, jsonify
import os
import json

app = Flask(__name__)

MP3_DIRECTORY = '../data/audiomp3'
STM_DIRECTORY = '../data/transcripts/cleanedtranscripts'
JSON_FILE_PATH = '../data/mappedtopics/selectedtopics.json'
TITLE_PATH = '../data/mappedtopics/maptitle.json'
IMAGE_PATH = '../data/images'

@app.route('/get-mp3')
def get_audio():
    filename = request.args.get('filename')  
    mp3_file_name = filename + '.mp3' 
    mp3_path = os.path.join(MP3_DIRECTORY, mp3_file_name)
    return send_file(mp3_path, mimetype='audio/mpeg', as_attachment=True) 

def extract_transcript_from_stm(stm_path):
    with open(stm_path, 'r') as file:
        transcript = file.read()
    transcript = transcript.replace('\n', '') 
    return transcript

@app.route('/get-stm')
def get_stm():
    filename = request.args.get('filename')  # Get filename from query parameter
    stm_filename = filename + '.stm' 
    stm_path = os.path.join(STM_DIRECTORY, stm_filename)
    transcript = extract_transcript_from_stm(stm_path)
    return transcript, 200

def get_data():
    with open(JSON_FILE_PATH, 'r') as file:
        data = json.load(file)

    categories = list(data.keys())  # Extract categories from the JSON keys
    category_filenames = {category: data[category] for category in categories}  # Extract filenames for each category

    return categories, category_filenames


@app.route('/data')
def get_categories_Data():
    with open(JSON_FILE_PATH, 'r') as file:
        data = json.load(file)

    # Extract categories from the JSON data
    categories = list(data.keys())

    return jsonify({"categories": categories})

@app.route('/data/categories', methods=['POST'])
def get_category_filenames():
    selected_categories = request.json.get('categories', [])

    # Get categories and category-filename mappings from the data
    _, category_filenames = get_data()
      
    for category in selected_categories:
        category_filenames = category_filenames.get(category, [])  # Get filenames associated with the selected category
    return jsonify(category_filenames)
@app.route('/images/<path:filename>')
def get_image(filename):
    image_file = None
    category = None

    for file in os.listdir(IMAGE_PATH):
        if filename in file and file.endswith('.png'):  # Check if 'filename' is part of 'file'
            image_file = file
            category = file.split('_')[0]  # Extract category from filename
            category = category.capitalize()  # Capitalize the category
            break

    if image_file:
        return send_from_directory(IMAGE_PATH, image_file), 200, {'Category': category}
    else:
        return "Image not found", 404



@app.route('/data/central-image', methods=['POST'])
def get_central_image():
    selected_categories = request.json.get('categories', [])
    central_image = None
    for file in os.listdir(IMAGE_PATH):
        for category in selected_categories:
            if category in file and file.endswith('_M.png'):
                central_image = file
                break

    if central_image:
        return send_from_directory(IMAGE_PATH, central_image)
    else:
        return "Image not found", 404

@app.route('/get-title', methods=['GET'])
def get_title():
    filename = request.args.get('filename', '')

    with open(TITLE_PATH, 'r') as f:
        data = json.load(f)

    for recording in data:
        if recording['baseFileName'] == filename:
            title = recording['title']
            return title

    return filename



if __name__ == '__main__':
    app.run(debug=True, port=15000)

