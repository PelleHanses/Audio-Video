#!/usr/bin/env python3

import os
import subprocess
import argparse

def run_ffmpeg_command(input_file, start_time, end_time):
    output_file = f'{os.path.splitext(input_file)[0]}.fixed.mp3'

    subprocess.run([
        'ffmpeg', '-i', input_file,
        '-ss', start_time,
        '-to', end_time,
        '-c', 'copy',
        output_file
    ], check=True)

def main():
    parser = argparse.ArgumentParser(description='Audio processing script')
    parser.add_argument('--audio', required=True, help='Path to the input audio file')
    parser.add_argument('--start', required=True, help='Start time in HH:MM:SS format')
    parser.add_argument('--end', required=True, help='End time in HH:MM:SS format')

    args = parser.parse_args()

    try:
        run_ffmpeg_command(args.audio, args.start, args.end)
        print("Audio processing completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during audio processing: {e}")

if __name__ == "__main__":
    main()

