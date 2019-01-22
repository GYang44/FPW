#/bin/bash 
#This script help convert stere audio file to mono chanel
ffmpeg -i $1 -c:v copy -c:a libmp3lame -ac 1 -q:a 2 $2
