#!/usr/bin/env python3

import os
import subprocess
import argparse

def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

def run_ffmpeg_silence_detection(input_file):
    # Run silence detection for both durations
    with open('silence_long.txt', 'w') as long_output:
        subprocess.run([
            'ffmpeg', '-i', input_file,
            '-af', 'silencedetect=noise=-30dB:d=2.0', '-f', 'null', '-'
        ], check=True, stderr=long_output)

    with open('silence_short.txt', 'w') as short_output:
        subprocess.run([
            'ffmpeg', '-i', input_file,
            '-af', 'silencedetect=noise=-30dB:d=2.0', '-f', 'null', '-'
        ], check=True, stderr=short_output)

def extract_segment_times():
    # Extract segment times from silence_short.txt
    segment_times = subprocess.check_output([
        'grep', '-oP', '(?<=silence_start: )[0-9.]+', 'silence_short.txt'
    ], text=True).strip().split('\n')

    return ','.join(segment_times)

def run_ffmpeg_segmentation(input_file, folder_name, new_name, segment_times):
    # Run ffmpeg segmentation with extracted segment times
    subprocess.run([
        'ffmpeg', '-i', input_file,
        '-map', '0', '-c', 'copy', '-f', 'segment',
        '-segment_times', segment_times,
        os.path.join(folder_name, f'{new_name}_%03d.mp3')
    ], check=True)

def main():
    parser = argparse.ArgumentParser(description='Audio processing script')
    parser.add_argument('--audio', required=True, help='Path to the input audio file')
    parser.add_argument('--foldername', required=True, help='Name of the new folder to save files in')
    parser.add_argument('--newname', required=True, help='Name of the new files (prefix for output files)')

    args = parser.parse_args()

    folder_name = args.foldername
    create_folder(folder_name)

    try:
        run_ffmpeg_silence_detection(args.audio)
        segment_times = extract_segment_times()
        run_ffmpeg_segmentation(args.audio, folder_name, args.newname, segment_times)
        print("Audio processing completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during audio processing: {e}")
    finally:
        # Remove silence.txt files
        try:
            os.remove('silence_long.txt')
        except OSError:
            pass

        try:
            os.remove('silence_short.txt')
        except OSError:
            pass

if __name__ == "__main__":
    main()

