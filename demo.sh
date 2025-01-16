
#!/bin/bash

CAST_FILE="demo.cast"
GIF_FILE="demo.gif"

# Start asciinema recording with automation using expect
expect << EOF
  spawn asciinema rec --headless --tty-size 127x35  -c \"pdm run ctodo -c ./config.toml\"  "$CAST_FILE"
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

