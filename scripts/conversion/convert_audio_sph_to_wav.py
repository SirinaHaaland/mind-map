import os
import subprocess

def convert_sph_to_wav(sph_path, wav_path):
    command = ["sox", sph_path, wav_path]
    subprocess.run(command, check=True)

def convert_all_sph_in_directory(source_directory, target_directory):
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    for file in os.listdir(source_directory):
        if file.endswith(".sph"):
            sph_path = os.path.join(source_directory, file)
            wav_filename = os.path.splitext(file)[0] + ".wav"
            wav_path = os.path.join(target_directory, wav_filename)
            print(f"Converting {sph_path} to {wav_path}")
            convert_sph_to_wav(sph_path, wav_path)
            print("Conversion complete.")

source_dir = "C:\\Users\\sirin\\DATBAC-1\\STG0006948\\data\\TEDLIUM_release-3\\TEDLIUM_release-3\\data\\sph"
target_dir = "C:\\Users\\sirin\\DATBAC-1\\STG0006948\\data\\audio_wav"

convert_all_sph_in_directory(source_dir, target_dir)

"""
How to Execute the Script:
First make sure that:
SoX is installed and added to PATH. This allows the subprocess.run(command, check=True) 
function to call SoX from anywhere without specifying its full installation path.
Change the following:
source_dir (path to the directory containing the .sph files)
target_dir (path to the directory where the .wav files will be saved)
Open a terminal in Visual Studio Code (Terminal > New Terminal).
Navigate to the script's directory if your terminal doesn't open there by default.
Run the script by typing python convert_audio_wav.py in the terminal.
The script will iterate over all files in the source_dir that end with .sph, convert 
each one to a WAV file using SoX, and save the resulting WAV files in target_dir. 
It will print a message for each file it converts, providing feedback on the conversion process.
"""
