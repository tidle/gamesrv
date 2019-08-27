# Gamesrv

Gamesrv is a game server using flask, socket.io, chess.js, and chessboard.js

It currently only supports chess, though I plan to add more games in the future

## Installing

1. Execute `install_packages.sh`
    - You need to run this with sudo
    - It only works on Ubuntu.  If you are using a different distribution, make sure python3, python3-pip, and python3-venv are installed before continuing to the next step
2. Execute `setup.sh`
    - This will automatically create a virtual environment, and install the required packages
    - It will not affect your global python environment

Done!
*Note: by default, the server only listens to connections from localhost, port 5000.  You can change this by modifying main.py, or connect it to another web server like nginx.*

## Running

1. Execute `run.sh`
    - You don't need to be in the virtual environment for this to work

Done!
You can stop it with control-C, or use it in headless mode with `./run.sh headless`

If you have started it in headless mode, you can stop it with `./run.sh stop`

## Viewing the log.txt file

You can use the `printlog.py` file to view the log file
Options:
- all, or move
    - output all the messages in the log file, including:
        - move
        - info
        - warn
- info
    - only output info and warn log messages
- warn
    - only output warnings