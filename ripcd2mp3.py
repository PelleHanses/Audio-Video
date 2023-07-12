#!/usr/bin/env python3

import sys
import subprocess
import os
from pydub import AudioSegment
from mutagen.id3 import ID3, TIT2, TPE1, TALB

def rip_cd_to_mp3(output_dir, title, artist, album, bitrate, tracknr):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Rip the audio CD tracks using cdparanoia
    subprocess.call(['cdparanoia', '-B'])

    # Get the list of WAV files in the current directory
    wav_files = [file for file in os.listdir('.') if file.endswith('.wav')]

    # Set the MP3 tags and convert to desired bitrate
    for wav_file in wav_files:
        #mp3_file = os.path.join(output_dir, os.path.splitext(wav_file)[0] + '.mp3')
        print("Track nr: " + str(tracknr))
        track_nr_string = str(tracknr).zfill(2)
        mp3_file_name = artist + " - " + track_nr_string + " - " + title + ".mp3"
        mp3_file = os.path.join(output_dir, f'{mp3_file_name}')

        # Convert the WAV file to MP3 using ffmpeg with desired bitrate
        subprocess.call(['ffmpeg', '-i', wav_file, '-b:a', bitrate, mp3_file])

        # Set the MP3 tags using mutagen
        title_new = track_nr_string + " " + title
        audio = ID3(mp3_file)
        audio['TIT2'] = TIT2(encoding=3, text=title_new)
        audio['TPE1'] = TPE1(encoding=3, text=artist)
        audio['TALB'] = TALB(encoding=3, text=album)
        audio.save()

        # Remove the WAV file
        os.remove(wav_file)

        tracknr += 1

# Extract command-line arguments
args = sys.argv[1:]
if len(args) < 7:
    print('Insufficient arguments! Usage: python rip_cd.py -o OUTPUT_DIR -t TITLE -a ARTIST -b ALBUM -r BITRATE -i FIRST_TRACK_NR')
    sys.exit(1)

# Parse command-line arguments
output_dir = args[args.index('-o') + 1]
title = args[args.index('-t') + 1]
artist = args[args.index('-a') + 1]
album = args[args.index('-b') + 1]
bitrate = args[args.index('-r') + 1]
#tracknr = args[args.index('-i') + 1]

# Calculate next track number
folder_path = output_dir + "/" + output_dir  # Replace with the path to your folder
tracknr = 1 

try:
    if not os.path.exists(folder_path):
        raise FileNotFoundError
    for filename in os.listdir(folder_path):
        if filename.endswith('.mp3'):
            tracknr += 1
except FileNotFoundError:
    tracknr = 1

print(tracknr)

# Change to the output directory
os.chdir(output_dir)

# Rip CD and set MP3 tags with desired bitrate
rip_cd_to_mp3(output_dir, title, artist, album, bitrate, int(tracknr))

print('CD ripped and MP3 tags set successfully.')

