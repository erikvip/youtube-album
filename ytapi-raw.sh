#!/bin/bash

# With a wget match, this line will extract video id, title and duration
# Also removes playlists and matches only videos
q="$*"
[ -z "$q" ] && echo "No search string specified" && exit 1


wget -q -O - "https://www.youtube.com/results?search_query=${q}" | 
	grep 'yt-lockup-content' | grep -v 'playlist-item-title' | sed -r 's/<a href="\/watch\?v\=(.{11})[^>]*?>/id:\1 title:/g' | sed -E 's/<[^>]*?>//g' | sed -E 's/ - Duration: ([0-9\:]*).*$/ time:\1/g'

#cat anjali.html | grep 'yt-lockup-content' | grep -v 'playlist-item-title' | sed -r 's/<a href="\/watch\?v\=(.{11})[^>]*?>/id:\1 title:/g' | sed -E 's/<[^>]*?>//g' | sed -E 's/ - Duration: ([0-9\:]*).*$/ time:\1/g'
#cat anjali.html | grep 'yt-lockup-content' | grep -v 'playlist-item-title' | sed -r 's/<a href="\/watch\?v\=(.{11})[^>]*?>/id:\1 title:/g' | sed -E 's/<[^>]*?>//g' | sed -E 's/ - Duration: ([0-9\:]*).*$/ time:\1/g'
