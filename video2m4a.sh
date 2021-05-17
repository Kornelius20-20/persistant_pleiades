#! /bin/bash

# Change cwd to folder where videos are
cd "New folder"

# Get the video files as list
a=$(ls)

# Change IFS to newline to have the for loop choose each file name separately
IFS='
'

# For each file, extract audio stream
for file in $a
do
	ffmpeg -i "$file" -vn "${file:0:-4}.m4a"
done

# Cleanup
unset IFS
