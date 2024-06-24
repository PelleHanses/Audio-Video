#!/usr/bin/env python3

import os
import subprocess
import argparse
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, ID3NoHeaderError

def clean_up():
    # Delete the script file executable
    command = "rm watch_process_wav.sh" 
    subprocess.run(command, shell=True, check=True)

def create_watch_script(watch_dir, script_file):
    print(f"  To follow progress, you can run the script \"watch ./{script_file}\" in another terminal. End it with Ctrl+C")
    bash_script_content = f'''#!/bin/bash
    ls -lth --time-style=long-iso "{watch_dir}" | awk '{{printf "\\"%s\\"   %s %s   %s\\n",substr($0, index($0,$8)),$6,$7,$5}}'
    '''
    # Write the content to the bash script file
    with open(script_file, 'w') as file:
        file.write(bash_script_content)
    # Do the script file executable
    command = "chmod u+x " + script_file
    subprocess.run(command, shell=True, check=True)

def rip_cd_to_wav(first_track_nr, wav_dir, verbose):
    create_watch_script(wav_dir, "watch_process_wav.sh")
    os.makedirs(wav_dir, exist_ok=True)
    track_nr = first_track_nr
    #return wav_dir
    if verbose >= 1:
            print(f"  + Ripping track:")
    while True:
        wav_file = os.path.join(wav_dir, f'track_{track_nr:02d}.wav')
        if verbose >= 1:
            print(f"    track_{track_nr:02d}.wav")
        result = subprocess.run(['cdparanoia', '-q', f'{track_nr}', wav_file], capture_output=True)
        if result.returncode != 0:
            break
        track_nr += 1
    # Eject the CD/DVD drive on Linux
    subprocess.run(['eject'], check=True)

    return wav_dir

def convert_wav_to_mp3(wav_dir, title, artist, album, output_dir, album_nr, mp3_bitrate, first_track_nr, start_track_num, skip_last, nr_length, verbose):
    if verbose >= 2:
        print(f"wav_dir: {wav_dir}")
        print(f"title: {title}")
        print(f"artist: {artist}")
        print(f"album: {album}")
        print(f"output_dir: {output_dir}")
        print(f"album_nr: {album_nr}")
        print(f"mp3_bitrate: {mp3_bitrate}")
        print(f"first_track_nr: {first_track_nr}")
        print(f"start_track_num: {start_track_num}")
        print(f"skip_last: {skip_last}")
        print(f"nr_length: {nr_length}")
        print(f"first_track_nr: {first_track_nr}")
    track_num = start_track_num
    wav_files = sorted(os.listdir(wav_dir))  # Sort the WAV files by their filenames
    print(f"  + Creating file:")
    for wav_file in wav_files:
        if wav_file.endswith('.wav'):
            wav_path = os.path.join(wav_dir, wav_file)
            if album_nr == 0:
                mp3_file = os.path.join(output_dir, f'{track_num:03d} - {title} - {album}.mp3')
                verbose_print = (f"{track_num:03d} - {title} - {album}.mp3")
            else:
                mp3_file = os.path.join(output_dir, f'{track_num:03d} - {title} - {album_nr}, {album}.mp3')
                verbose_print = (f"{track_num:03d} - {title} - {album_nr}, {album}.mp3")
            if verbose >= 1:
                print(f"    {verbose_print}")


            # Convert WAV to MP3
            subprocess.run(['lame', '--quiet', '--preset', mp3_bitrate, wav_path, mp3_file])

            # Check if the MP3 file was created successfully
            if os.path.exists(mp3_file):
                try:
                    audio = EasyID3(mp3_file)
                except ID3NoHeaderError:
                    audio = EasyID3()
                    audio.save(mp3_file)

                audio['title'] = f'{track_num:02d} - {title}'
                audio['artist'] = artist
                if album_nr == 0:
                    audio['album'] = album
                else:
                    audio['album'] = album_nr + ", " + album
                audio['tracknumber'] = str(track_num)
                if verbose >= 2:
                    print(f"      Setting mp3 info")
                audio.save(mp3_file)

            track_num += 1

def main():
    parser = argparse.ArgumentParser(description='Rip audio CD to MP3 files with metadata.')
    parser.add_argument('--title', type=str, required=True, help='Title of the tracks.')
    parser.add_argument('--artist', type=str, required=True, help='Artist name')
    parser.add_argument('--album', type=str, required=True, help='Album name')
    parser.add_argument("--output_dir", type=str, required=True, help="The output directory for processed mp3 files.")

    parser.add_argument("--album_nr", type=str, default=0, help="Optional. Number of the album. Default is none.")
    parser.add_argument('--mp3_bitrate', type=str, default='256k', help='Optional. MP3 bitrate (e.g., 192k, 256k, 320k), default is 256k.')
    parser.add_argument('--first_track_nr', type=int, default=1, help='Optional. First track number to start ripping from (e.g., 2 to skip the first track). Default is 1.')
    parser.add_argument('--start_track_num', type=int, default=1, help='Optional. Starting track number for naming purposes. Default is 1.')
    parser.add_argument("--skip_last", type=str, choices=['yes', 'no'], default='no', help="Optional. Skip the last track (yes/no). Default is 'no'.")
    parser.add_argument("--nr_length", type=int, default=3, help="Optional. Number length for track numbering. Default is 3.")
    parser.add_argument("--verbose", type=int, default=0, help="Optional. Show more info. (0/1/2)")


    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    wav_dir = os.path.join(args.output_dir, 'wav_files')
    rip_cd_to_wav(args.first_track_nr, wav_dir, args.verbose)

    convert_wav_to_mp3(wav_dir, args.title, args.artist, args.album, args.output_dir, args.album_nr, args.mp3_bitrate, args.first_track_nr, args.start_track_num, args.skip_last, args.nr_length, args.verbose)

    for wav_file in os.listdir(wav_dir):
        print(f"  Deletes file {wav_file} in {wav_dir,}.")
        os.remove(os.path.join(wav_dir, wav_file))
    os.rmdir(wav_dir)

    clean_up()

if __name__ == '__main__':
    main()

