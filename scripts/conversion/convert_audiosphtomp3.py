import os
import subprocess

def convert_sph_to_mp3(sph_path, mp3_path):
    command = ["sox", sph_path, "-C", "192", mp3_path]  # "-C 192" sets the MP3 quality
    subprocess.run(command, check=True)

def convert_all_sph_in_directory(source_directory, target_directory):
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    file_count = 0  

    for file in os.listdir(source_directory):
        if file.endswith(".sph"):
            sph_path = os.path.join(source_directory, file)
            mp3_filename = os.path.splitext(file)[0] + ".mp3"
            mp3_path = os.path.join(target_directory, mp3_filename)
            convert_sph_to_mp3(sph_path, mp3_path)
            file_count += 1  
            print(file_count)
    print(f"Conversion complete. {file_count} files were converted.")

source_dir = "../../data/sph" # Empty folder, upload your sph files her
target_dir = "../../data/audiomp3" # Contains the converted TEDLIUM 3 audio files now

convert_all_sph_in_directory(source_dir, target_dir)

"""
How to Execute the Script:
First make sure that:
SoX is installed and added to PATH. This allows the subprocess.run(command, check=True) 
function to call SoX from anywhere without specifying its full installation path. Follow link:
https://sourceforge.net/projects/sox/. 
Additional LAME library needed for SoX to convert to mp3. Comes as a zip file, needs to be 
decompressed at the same location as SoX. Follow link:
https://www.rarewares.org/mp3-lame-libraries.php. Choose the libmp3lame 3.100, x86-Win32 (336kB.) option. 
Change the following:
source_dir (path to the directory containing the .sph files)
target_dir (path to the directory where the .mp3 files will be saved)
Open a terminal in Visual Studio Code (Terminal > New Terminal).
Navigate to the script's directory if your terminal doesn't open there by default.
Run the script by typing python convertaudiosphtomp3.py in the terminal.
The script will iterate over all files in the source_dir that end with .sph, convert 
each one to a mp3 file using SoX, and save the resulting mp3 files in target_dir. 
It will print the count for each file and a message when conversion is complete.
"""
