#!/bin/bash

# Poor man's search api through a scraper
# To get around the gay quota limit

keyword="$1"
outfile=$(tempfile); 
URL="https://www.youtube.com/results?search_query=${keyword}"

echo "Searching for ${keyword}" >> log.txt
echo "${URL}" >> log.txt

#jsonfile=$(tempfile);

wget -q -O "${outfile}" "${URL}";


#wget -q -O "${outfile}"  'https://www.youtube.com/results?search_query=${keyword}'

#	grep -Po '(<span aria-label="[^"]*">.*?</span>|href="/watch[^"]*")' | \

cat "${outfile}" | \
	grep 'yt-lockup-content' | \
	grep -Po '(<span aria-label="[^"]*">.*?</span>|href="/watch[^"]*")' | \
	tr "\n" " " | \
	sed 's/<\/span>/\
/g' | \
	sed -e 's/^ href/href/g' | \
	sed -e 's/^href="\/watch?v=\([^"]{12}\)" <span aria-label="[^"]*">\(.*\)/\1 \2/g' 
#	sed -e 's/^href="\/watch?v=\([^"]*\)" <span aria-label="[^"]*">\(.*\)/\1 \2/g' 
#	sed -e 's/^href="\/watch?v=\([^"]*\)" <span aria-label="[^"]*">\(.*\)/id:"\1",title:"\2"/g' 
#	sed -e 's/^/\{/g' -e 's/$/\},/g' |
#	grep -v "^\{ \},$" 

#echo "{data:[" `cat "${jsonfile}"` "]}"

#rm "${jsonfile}"



rm "${outfile}"


#	grep 'yt-lockup-content' | grep '(<span aria-label="[^"]*">.*?</span>|href="/watch[^"]*")' | tr "\n" " " | sed 's/<\/span>/\
#/g' | sed -e 's/^ href/href/g' | sed -e 's/^href="\/watch?v=\([^"]*\)" <span aria-label="[^"]*">\(.*\)/id="\1",title="\2"/g'  | sed -e 's/^/\{/g' -e 's/$/\},/g'
