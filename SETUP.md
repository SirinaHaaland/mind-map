# Setup Instructions

This document provides the instructions needed to set up and run the system. It covers software prerequisites, installation steps, and how to get the application running in a development environment.

## Prerequisites

Before you begin, ensure your system meets these prerequisites:

- **Python:** Backend development language. [Download Python](https://www.python.org/downloads/)
- **Node.js and npm:** Manage React application dependencies. [Download Node.js](https://nodejs.org/)
- **Flask:** Python micro Web framework. Install with `pip install flask`.
- **React:** Frontend development framework. Setup with `npx create-react-app`.

### Additional Libraries and Tools

- **SoX (Sound eXchange):** For audio processing tasks. [Download SoX](https://sourceforge.net/projects/sox/)
- **LAME MP3 Encoder:** For MP3 encoding with SoX. [Download LAME](https://www.rarewares.org/mp3-lame-libraries.php)
- **React Libraries:** Packages for UI components and HTTP requests.
  - Axios: `npm install axios`
  - Material-UI: `npm install @mui/material @emotion/react @emotion/styled`
  - Image Cropping Tool: `npm install uui`
- **Data Processing and Machine Learning Libraries:**
  - NLTK: `pip install nltk`
  - Scikit-Learn: `pip install scikit-learn`
  - Gensim: `pip install gensim`
  - Hugging Face Transformers: `pip install transformers`
  - Novita.ai: `pip install novita`
  - OpenAI: `pip install openai`
- **Plotting Results:**
  - Matplotlib: `pip install matplotlib`

## Installation

Clone the repository to get started:

git clone https://github.com/SirinaHaaland/STG0006948.git


## Running the Application

To run the application in a development environment, follow these steps:

1. **Start the Flask Backend:**
   - Navigate to the `flask-server` directory.
   - Run `python server.py`.
   - The server will start on `localhost:5000`.

2. **Run the React Frontend:**
   - Navigate to the `client` directory.
   - Execute `npm start`.
   - This opens a browser tab at `localhost:3000`, connected to your Flask backend.
