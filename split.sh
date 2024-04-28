#/bin/bash

# sudo apt install -y ffmpeg
# sudo apt install -y kid3-cli
# sudo apt install -y mp3blaster
# sudo apt install -y mp3splt
# sudo apt-get install -y python3-mutagen
# sudo apt-get install -y ffmpeg kid3-cli mp3blaster mp3splt python3-mutagen

ORIGINAL_FIL="Example-serie 02 Book2.mp3"
MP3_ARTIST="Example-serie"
MP3_TITEL="Book2"
MP3_TITEL_NR="02_" # End with "_"
NYTT_NAMN="$MP3_TITEL - $MP3_ARTIST.mp3"

#ffmpeg -i "$ORIGINAL_FIL" -f segment -segment_time 600 -c copy "%02d_$MP3_TITEL.mp3"
#mp3splt -f -s -p -min=3 -o @n_@f $ORIGINAL_FIL
# mp3splt -f -s th=40,min=120 -o @n_"$NYTT_NAMN" "$ORIGINAL_FIL"
#echo NT = Antal kapitel
mp3splt -f -s -p th=40,nt=12 -o "$MP3_TITEL_NR"@n" - $NYTT_NAMN" "$ORIGINAL_FIL"


for file in [0-9]*.mp3; do
	FIL_NUMMER=$(echo $file | awk -F" - " '{print $1}')	
	mp3tag \
	-a "$MP3_ARTIST" \
	-s "$FIL_NUMMER-$MP3_TITEL" \
	-l "$MP3_TITEL" \
	-k "$FIL_NUMMER" \
	"$file"
	# mp3tag sätter endast IDv1 medans mid3v2 sätter IDv2
	mid3v2 \
	--artist="$MP3_ARTIST" \
	--album="$MP3_TITEL_NR$MP3_TITEL" \
	--song="$FIL_NUMMER - $MP3_TITEL" \
	--track="$FIL_NUMMER" \
	"$file"
	
	
done
#-s "${file%.*}" \

