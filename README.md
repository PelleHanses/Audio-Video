# Audio-Video
Small scripts for audio and video

## ripaudibookocd2mp3.py
Rip audio book CD to MP3 files with metadata. Rips CD with CDparanoia. \
usage: ripaudiocd2mp3.py [-h] --title TITLE --artist ARTIST --album ALBUM --output_dir OUTPUT_DIR [--album_nr ALBUM_NR] [--mp3_bitrate MP3_BITRATE] [--first_track_nr FIRST_TRACK_NR]
                         [--start_track_num START_TRACK_NUM] [--skip_last {yes,no}] [--nr_length NR_LENGTH] [--verbose VERBOSE]

Minimal start: \
```
./ripaudibookocd2mp3.py --output_dir My_Folder --title My_Audio_Book --artist Writer --album Book_Serie
```

Options:
  -h, --help                        Show this help message and exit
  --title TITLE                     Title of the tracks.
  --artist ARTIST                   Artist name
  --album ALBUM                     Album name
  --output_dir OUTPUT_DIR           The output directory for processed mp3 files.

  --album_nr ALBUM_NR               Optional. Number of the album. Default is none.
  --mp3_bitrate MP3_BITRATE         Optional. MP3 bitrate (e.g., 192k, 256k, 320k), default is 256k.
  --first_track_nr FIRST_TRACK_NR   Optional. First track number to start ripping from (e.g., 2 to skip the first track). Default is 1.
  --start_track_num START_TRACK_NUM Optional. Starting track number for naming purposes. Default is 1.
  --skip_last {yes,no}              Optional. Skip the last track (yes/no). Default is 'no'.
  --nr_length NR_LENGTH             Optional. Number length for track numbering. Default is 3.
  --verbose VERBOSE                 Optional. Show more info. (0/1/2)
