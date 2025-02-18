# **INSTRUCTIONS.md**

## **Overview**

This document provides detailed instructions for processing a new speech collection using the **Mind Map** pipeline. It covers the steps needed to:

- Convert audio files
- Clean transcripts
- Apply topic modeling
- Refine topics using GPT-3.5
- Merge duplicate topics
- Generate AI-enhanced images
- Integrate results into the **Mind Map** application

For general installation instructions, refer to **SETUP.md**.

## **Prerequisites**

Ensure you have set up all required dependencies as outlined in **SETUP.md**, including:

- **Python** and necessary libraries
- **Node.js** and **React** for frontend
- **Flask** for backend
- **SoX** for audio conversion
- **OpenAI API key** for GPT-3.5 topic refinement
- **Novita AI API key** for image generation

## **Dataset Preparation**

Place your raw SPH audio files in:

```
data/sph/
```

Place your raw transcripts in:

```
data/transcripts/rawtranscripts/
```

Ensure the directory structure matches the expected format:

```
data/
├── audiomp3
├── images/
├── mappedtopics/
│   ├── gpt-3_5topicmappings.json
│   ├── maptitle.json
│   ├── mergedgpt-3_5topicmappings.json
│   ├── selectedtopics.json
├── sph/
├── transcripts/
│   ├── rawtranscripts/
│   ├── cleanedtranscripts/
```

---

### **Metadata File: `maptitle.json` (Required for Titles & Authors)**

The file **`maptitle.json`** contains metadata for each audio file and transcript, mapping them to titles and authors. This enhances the frontend display by showing meaningful titles instead of just filenames.

#### **Format of `maptitle.json`**
```json
[
    {
        "Identifier": "DavidPogue_2006",
        "Title": "David Pogue: says 'Simplicity sells'"
    },
    {
        "Identifier": "MajoraCarter_2006",
        "Title": "Majora Carter: Greening the ghetto"
    },
    {
        "Identifier": "SirKenRobinson_2006",
        "Title": "Ken Robinson: says schools kill creativity"
    }
]
```

#### **Why is this file important?**
- The frontend retrieves titles and authors via the API endpoint:
 `/get-title?filename={filename}`

- Without **`maptitle.json`**, the UI will display only filenames instead of proper titles and author names.
- The backend **does not generate this file**, so it must be manually created or sourced.

#### **What if I don’t have a `maptitle.json` file?**
- If missing, the application will **still work**, but **titles and authors will not be displayed**—only filenames.
- You must **create or source** a similar file formatted like the example above.
- A **sample `maptitle.json`** is included in the repository. Replace this with your own metadata.

```
data/mappedtopics/maptitle.json
```

📌 **Note:** If your dataset does not include metadata like this, you may need to modify the `/get-title` route in the Flask backend to handle missing metadata gracefully.


## **Step-by-Step Processing**

### **1. Convert Audio Files (SPH to MP3)**

Run the following script to convert `.sph` files to `.mp3`:

```bash
python scripts/conversion/convert_audiosphtomp3.py
```

Ensure **SoX** is installed and added to `PATH`.

Converted `.mp3` files will be saved in:

```
data/audiomp3/
```

### **2. Clean Transcripts**

Run the text cleaner script:

```bash
python scripts/textcleaner/simpletextcleaner.py
```

This removes `<NA>` markers and deletes everything before them (used for speaker metadata in STM transcripts), and `<unk>` tokens (representing unrecognized words). This script is optimized for STM transcripts (like those in data/transcripts/rawtranscripts/). If your transcripts don’t use <NA> or store timestamps differently, you may need to modify simpletextcleaner.py to avoid deleting important content.

Cleaned transcripts are saved in:

```
data/transcripts/cleanedtranscripts/
```

### **3. Topic Modeling (TF-IDF + K-Means Clustering)**

Run the custom topic modeling script:

```bash
python scripts/topicmodeling/custom/custom.py
```

📌 **How to use this script interactively:**
- The script will **display identified topics** and associated transcripts based on the dataset.
- You will be prompted to **review and select** topics to keep.
- If you select a topic, its associated transcripts will be categorized under it.
- If a topic is not selected, its transcripts will be reprocessed in a later run.
- You will also be prompted to **update the stopwords list** as unnecessary words may appear as topics. The stopwords list is a file (customstopwords.txt) stored in `scripts/topicmodeling/custom/`, containing words that should be ignored during topic modeling. Common stopwords include words like "the," "and," "is", but you may also want to exclude other frequently occurring but non-informative words. You can add new stopwords interactively when prompted during topic modeling. The list is updated and saved so it persists for future runs. If customstopwords.txt does not exist, the script automatically creates it using NLTK’s default English stopwords. You may also manually edit customstopwords.txt to include domain-specific words.

After finalizing topic selection, the script saves `selectedtopics.json` in:

```
data/mappedtopics/
```

The custom script supports pausing and resuming, allowing users to continue topic selection across multiple runs. If `selectedtopics.json` already exists, the script will automatically load its contents, ensuring that previously selected topics are retained and preventing duplicate processing of the same transcripts. This allows users to iteratively refine topics without losing progress.

### **4. GPT-3.5 Topic Refinement**

Run GPT-3.5 topic categorization:

```bash
python scripts/topicmodeling/gpt-3_5/gpt-3_5.py
```

✅ **Inputs:**
- Requires an **OpenAI API key**.
- This script assigns more refined topic categories to each transcript.

✅ **Output:**
- Generates `gpt-3_5topicmappings.json` in:

```
data/mappedtopics/
```

### **5. Merge Duplicate Topics**

Before generating images, merge duplicate topic names to avoid redundant entries. This script reads `gpt-3_5topicmappings.json`, which maps topics (keys) to lists of files (values). It uses seen_keys = {} to store existing topic names in lowercase to prevent case-sensitive duplicates (e.g., "AI" and "ai" are treated as the same topic). If a topic already exists, the new values are appended to the original key, otherwise, the topic is added as a new entry.

Run:

```bash
python scripts/topicmodeling/gpt-3_5/merge_duplicates.py
```

✅ **Output:**
- Creates `mergedgpt-3_5topicmappings.json` in `data/mappedtopics/`, ensuring topics are correctly merged before image generation.

### **6. Generate Images for Topics (Novita AI)**

Topics are visualized as interactive clusters where each node links to an audio recording and transcript.

#### **Generate Main Topic Images**  
This generates **one** image per topic (from `selectedtopics.json`). These images are used for visualizing central nodes in the frontend.

```bash
python scripts/imagegeneration/novitaaimaintopics.py
```

✅ **Inputs:**  
- Uses `selectedtopics.json` (Topics identified in custom script)  
- Reads from `data/mappedtopics/selectedtopics.json`

✅ **Output:**  
- Saves images to `data/images/`
- Filenames: `{category}_M.png` (e.g., `Technology_M.png`)

#### **Generate Images for Individual Transcripts**  
This generates **one** image per **transcript** (from `mergedgpt-3_5topicmappings.json`). These images are used for visualizing sub-nodes (surrounding the central node). These images are also displayed on the mainrec page alongside the audio playback and transcript viewer.

```bash
python scripts/imagegeneration/novitaaipt3_5.py
```

✅ **Inputs:**  
- Uses `mergedgpt-3_5topicmappings.json` (GPT-3.5 generated topics)  
- Reads from `data/mappedtopics/mergedgpt-3_5topicmappings.json`

✅ **Output:**  
- Saves images to `data/images/`
- Filenames: `{category}_{filename}.png` (e.g., `Technology_file1.png`)

### **7. UI Assets (Background Images & Icons)**

The Mind Map UI uses custom images for the background and branding elements. 
The background images should be stored in:

```
data/
├── backgroundImage.png
├── backgroundImage2.png
```
These images are referenced in the CSS styles for the frontend UI. If you need to replace these background images, place the files in `data/` and ensure the CSS paths are correct.

Custom UI assets such as icons and logos are stored in:
```
public/
├── favicon.ico
├── index.html
├── logo192.png
├── logo512.png
```
These assets are used for branding and browser tab icons. If changes are needed, update the files in the `public/` directory.

### **8. Integrate Results into Mind Map**

1. Ensure that the following files exist in `data/mappedtopics/`:
   ```plaintext
   selectedtopics.json
   mergedgpt-3_5topicmappings.json
   ```
2. Ensure `data/images/` contains the generated images.

3. Restart the application:

   ```bash
   cd flask-server && python server.py &
   cd ../client && npm start
   ```

4. Navigate to `localhost:3000` to view results.

## **Running the Full Pipeline**

To automate the entire process, run the following commands sequentially:

```bash
python scripts/conversion/convert_audiosphtomp3.py
python scripts/textcleaner/simpletextcleaner.py
python scripts/topicmodeling/custom/custom.py
python scripts/topicmodeling/gpt-3_5/gpt-3_5.py
python scripts/topicmodeling/gpt-3_5/merge_duplicates.py
python scripts/imagegeneration/novitaaimaintopics.py
python scripts/imagegeneration/novitaaipt3_5.py
```

## **Troubleshooting & FAQs**

### **1. SoX Not Found Error**
- Ensure **SoX** is installed and added to `PATH`.

### **2. OpenAI API Key Error**
- Ensure your API key is set in `gpt-3_5.py`.

### **3. Novita AI Image Generation Issues**
- Verify API key and check `data/mappedtopics/selectedtopics.json` exists.

For additional questions, refer to **README.md** or contact **2024mindmap@gmail.com**.

