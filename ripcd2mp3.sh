#!/bin/bash
# ripcd2mp3.sh
echo
echo "* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *"
echo "  Ripping CD to mp3."
echo "  Mp3 files are stored in folder named with book name."
echo "  Wav files are deleted."
echo "  Mp3 tags included"
echo
echo "  Use:"
echo "    ./ripcd2mp3.sh Book_serie Book_nr Book_name CD_nr Skip_first(true/false)"
echo
echo "       1 - Book serie"
echo "       2 - Book number in serie. 0 = do not use"
echo "       3 - Book name (in serie)"
echo "       4 - CD number in serie. 0 = do not use"
echo "       5 - Skip_first. The first audio file are skipped. True or false"
echo
echo "* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *"


book_serie="$1"
book_nr=$2
book_name="$3"
track_name="Avsnitt_"
cd_nr=$4
track_nr=1
skip_first=$5

# Check if help wanted
if [ "$1" == "--help" ]
then
    exit 1
fi
# Check that 5 arguments loaded
if [ "$#" -ne 5 ]
then
  echo "Incorrect number of arguments"
  exit 1
fi

if [ $book_serie > 0 ]
then
    mp3_folder="$book_serie/$book_nr - $book_name"
else
    mp3_folde=$book_name
fi
mkdir -p ./"$mp3_folder"
cd ./"$mp3_folder"

# Rip CD to wav
cdparanoia -B

for file in ./*.wav
do
  if [ $track_nr == 1 ] && [ $skip_first == true ] 
  then
   skip_first=false  
   rm "$file"
  else
    # Convert wav to mp3
    lame -m j -b 256 "$file" 

    # Adding leading zero's for variables
    cd_nr_zero=$(printf "%02d" $cd_nr)
    track_name_start=$(printf "%02d" $track_nr)    
    if [ $cd_nr > 0 ]
    then
        track_name_start="$cd_nr_zero - $track_name_start"
    fi

    filename=$(basename -- "$file")
    extension="${filename##*.}"
    filename="${filename%.*}"

    # Sätter taggar
    mp3tag \
  	-a "$book_serie" \
  	-s "$track_name_start - $book_nam" \
  	-l "$track_name_start - $book_name" \
  	-k "$track_name_start" \
  	"$track_name_start - $book_name.mp3"
  	# mp3tag sätter endast IDv1 medans mid3v2 sätter IDv2
    mid3v2 \
  	--artist="$book_serie" \
  	--album="$book_nr - $book_name" \
  	--song="$track_name_start - $book_name.mp3" \
  	--track="$track_name_start" \
  	"$track_name_start - $book_name.mp3"

    mv "$filename.mp3" "$track_name_start - $book_name.mp3"

    track_nr=$((track_nr+1))
  fi
done
rm -fr ./*.wav
