# Audio-Video
Small scripts for audio and video

## ripcd2mp3.py
Rips CD to wav, converts it to mp3 and deletes the wav files.
If multiple CD:s, for example a audio book, the script will check how many files already ripped and name the files with next number in order.
Run it from the command line using the following format:
```
./ripcd2mp3.py -o OUTPUT_DIR -t TITLE -a ARTIST -b ALBUM -r BITRATE
```
For example:
```
./ripcd2mp3.py -o /path/to/output -t "Title" -a "Artist" -b "Album" -r 256k
```
Replace the placeholders with the appropriate values:
- OUTPUT_DIR: The directory where the MP3 files will be saved.
- TITLE: The title to set for all audio tracks.
- ARTIST: The artist to set for all audio tracks.
- ALBUM: The album name to set for all audio tracks.
- BITRATE: The desired output bitrate, e.g., "256k" for 256kb/s.
