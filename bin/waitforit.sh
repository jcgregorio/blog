#!/bin/bash
#!/bin/sh
while inotifywait -r -e modify ./news/; do
  echo "Making"
  make
done
