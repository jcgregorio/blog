#!/bin/bash

# Convert all HTML content into the form that jekyll expects.
#
# Note: Set YAML upfront permalink for all the top level .html files.

for i in $(find -name \*.html); do # Not recommended, will break on whitespace
  filename=$(basename "$i")
  extension="${filename##*.}"
  filename="${filename%.*}"
  date=`cat $i | grep "\<meta" | grep -o '[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}'`
  target=$date-$filename.html
  title=`grep -Pzo "(?s)(?<=\<title\>).+(?=\<\/title\>)" $i | tr -d '\n\r\t\f":'`
  body=`grep -Pzo "(?s)(?<=\<body\>).+(?=\<\/body\>)" $i`
  printf "\n---\nlayout: post\ntitle: %s\n---\n" "$title"
  echo ../../newblog/_posts/$date-$filename.html
  extra=""
  if [[ $i == *"/ga/"* ]]; then
    extra=`printf "permalink: /news/ga/$filename.html\n"`
  fi

  printf "%s\nlayout: post\ntitle: %s\n%s\n---\n" "---" "$title" "$extra" > ../../newblog/_posts/$date-$filename.html
  echo "$body" >>  ../../newblog/_posts/$date-$filename.html
done
