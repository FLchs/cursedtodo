
#!/bin/bash

# Check dependencies
if ! command -v asciinema &> /dev/null; then
  echo "Error: asciinema is not installed."
  exit 1
fi

if ! command -v agg &> /dev/null; then
  echo "Error: agg is not installed."
  exit 1
fi

if ! command -v expect &> /dev/null; then
  echo "Error: expect is not installed."
  exit 1
fi

# Output file for asciinema recording
CAST_FILE="demo.cast"
GIF_FILE="demo.gif"

# Start asciinema recording with automation using expect
expect << EOF
  spawn asciinema rec --headless --tty-size 127x35  -c "pdm run ctodo -c ./config.toml"  "$CAST_FILE"
  expect {
    "*" {
      sleep 3
      send "j"
      sleep 0.5
      send "j"
      sleep 0.5
      send "j"
      sleep 0.5
      send "\r"
      sleep 2
      send "q"
      sleep .5
      send "j"
      sleep 0.5
      send "j"
      sleep 2
      send "n"
      sleep .5
      send "OC"
      sleep .5
      send "OC"
      sleep .5
      send "OC"
      sleep 1
      send "	"
      sleep .2
      send "R"
      sleep .2
      send "e"
      sleep .2
      send "c"
      sleep .2
      send "o"
      sleep .2
      send "r"
      sleep .2
      send "d"
      sleep .2
      send " "
      sleep .2
      send "d"
      sleep .2
      send "e"
      sleep .2
      send "m"
      sleep .2
      send "o"
      sleep .2
      send "	"
      sleep .2
      send "OC"
      sleep .5
      send "OC"
      sleep .5
      send "OC"
      sleep .5
      send "OC"
      sleep .2
      send "	"
      sleep .2
      send "	"
      sleep .2
      send "d"
      sleep .2
      send "e"
      sleep .2
      send "v"
      sleep .2
      send ","
      sleep .2
      send " "
      sleep .2
      send "d"
      sleep .2
      send "e"
      sleep .2
      send "m"
      sleep .2
      send "o"
      sleep .2
      send "	"
      sleep .2
      send "c"
      sleep .2
      send "o"
      sleep .2
      send "m"
      sleep .2
      send "p"
      sleep .2
      send "u"
      sleep .2
      send "t"
      sleep .2
      send "e"
      sleep .2
      send "r"
      sleep .2
      send "	"
      sleep .2
      send "I"
      sleep .2
      send " "
      sleep .2
      send "n"
      sleep .2
      send "e"
      sleep .2
      send "e"
      sleep .2
      send "d"
      sleep .2
      send " "
      sleep .2
      send "t"
      sleep .2
      send "o"
      sleep .2
      send " "
      sleep .2
      send "r"
      sleep .2
      send "e"
      sleep .2
      send "c"
      sleep .2
      send "o"
      sleep .2
      send "r"
      sleep .2
      send "d"
      sleep .2
      send " "
      sleep .2
      send "a"
      sleep .2
      send " "
      sleep .2
      send "d"
      sleep .2
      send "e"
      sleep .2
      send "m"
      sleep .2
      send "o"
      sleep .2
      send " "
      sleep .2
      send "!"
      sleep .2
      send "	"
      sleep 1
      send "\r"
      sleep .2
      send "j"
      sleep .5
      send "j"
      sleep 0.5
      send "x"
      sleep 1.0
      send "\r"
      sleep 0.5
      send "j"
      sleep 3
      exit
    }
  }
EOF

# Check if the cast file was created
if [ ! -f "$CAST_FILE" ]; then
  echo "Error: Asciinema recording failed."
  exit 1
fi

# Convert the cast file to a GIF using agg
agg  --theme "solarized-dark"  "$CAST_FILE" "$GIF_FILE"
# rm "$CAST_FILE"

# Check if the GIF was created
if [ -f "$GIF_FILE" ]; then
  echo "GIF created successfully: $GIF_FILE"
else
  echo "Error: Failed to create GIF."
  exit 1
fi




