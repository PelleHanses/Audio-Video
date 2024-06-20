#!/usr/bin/env python3

import os
import subprocess
import argparse
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, ID3NoHeaderError

def rip_cd_to_wav(first_track_nr, wav_dir):
    os.makedirs(wav_dir, exist_ok=True)
    track_nr = first_track_nr
    #return wav_dir
    while True:
        wav_file = os.path.join(wav_dir, f'track_{track_nr:02d}.wav')
        result = subprocess.run(['cdparanoia', '-q', f'{track_nr}', wav_file], capture_output=True)
        if result.returncode != 0:
            break
        track_nr += 1
    return wav_dir

def convert_wav_to_mp3(wav_dir, output_dir, title, artist, album, mp3_bitrate, start_track_num):
    track_num = start_track_num
    wav_files = sorted(os.listdir(wav_dir))  # Sort the WAV files by their filenames
    for wav_file in wav_files:
        if wav_file.endswith('.wav'):
            wav_path = os.path.join(wav_dir, wav_file)
            mp3_file = os.path.join(output_dir, f'{track_num:02d} - {title} - {album}.mp3')

            # Convert WAV to MP3
            subprocess.run(['lame', '--quiet', '--preset', mp3_bitrate, wav_path, mp3_file])

            # Check if the MP3 file was created successfully
            if os.path.exists(mp3_file):
                try:
                    audio = EasyID3(mp3_file)
                except ID3NoHeaderError:
                    audio = EasyID3()
                    audio.save(mp3_file)

                audio['title'] = f'{track_num:02d} {title}'
                audio['artist'] = artist
                audio['album'] = album
                audio['tracknumber'] = str(track_num)
                audio.save(mp3_file)

            track_num += 1

def main():
    parser = argparse.ArgumentParser(description='Rip audio CD to MP3 files with metadata.')
    parser.add_argument('--title', type=str, required=True, help='Title of the tracks')
    parser.add_argument('--artist', type=str, required=True, help='Artist name')
    parser.add_argument('--album', type=str, required=True, help='Album name')
    parser.add_argument('--output_dir', type=str, required=True, help='Output directory for MP3 files')
    parser.add_argument('--mp3_bitrate', type=str, required=True, help='MP3 bitrate (e.g., 192k, 256k, 320k)')
    parser.add_argument('--first_track_nr', type=int, required=True, help='First track number to start ripping from (e.g., 2 to skip the first track)')
    parser.add_argument('--start_track_num', type=int, required=True, help='Starting track number for naming purposes')

    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    wav_dir = os.path.join(args.output_dir, 'wav_files')
    rip_cd_to_wav(args.first_track_nr, wav_dir)

    convert_wav_to_mp3(wav_dir, args.output_dir, args.title, args.artist, args.album, args.mp3_bitrate, args.start_track_num)

    for wav_file in os.listdir(wav_dir):
        os.remove(os.path.join(wav_dir, wav_file))
    os.rmdir(wav_dir)

if __name__ == '__main__':
    main()

