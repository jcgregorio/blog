#!/bin/bash

# Convert all HTML content into the form that jekyll expects.
#
# Note: Set YAML upfront permalink for all the top level .html files.

for i in $(find -name \*.html); do # Not recommended, will break on whitespace
  filename=$(basename "$i")
  extension="${filename##*.}"
  filename="${filename%.*}"
  date=`cat $i | grep "\<meta" | grep -o '[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}'`
  echo $date-$filename.html
done
