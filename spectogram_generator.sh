#!/bin/bash
#for id in songs/*.mp3
#do
#NAME=$("${id}" | cut -d "." -f1 | cut -d "/" -f2)
#echo -e "${NAME}.mp3" | sox "songs/${NAME}.mp3" -n spectrogram -o "spectograms/${NAME}.png" -r -h -x 800 -y 300
#done

for id in songs/*.mp3
do
    out="${id%.*}"
    out=$(basename $out)
    echo -e "$out.mp3" | sox songs/$out.mp3 -n remix - spectrogram -o spectrograms/$out.png -x 3000
done