# Pi-Camera-Streamer

This is a simple video streamer for use with the Pi Camera.  It streams video in mjpg format.
It is particularly useful when you want to same video feed to be consumed by more than one application.  For example a timelapse recording application and to also monitor in real time.


It is an adaptation of this work:
http://picamera.readthedocs.io/en/latest/recipes2.html#web-streaming

It was updated to use threadingHTTPServer and SimpleHTTPhandleror as well as allowing configuration from the command line

Its written using Python3

## Installation

1. Install dependencies:
    - `sudo apt-get update`
    - `sudo apt-get install python-picamera python3-picamera`
    
2. Download the streaming script to a directory of your choice.

    `wget https://github.com/stuartofmt/Pi-Camera-Streamer/raw/main/stream.py  -O stream.py`

3. Then make it executable

    `chmod 744 stream.py`

## Running stream.py

    python3 stream.py -port [-host] [-rotate]

Arguments:

- Specifying a `-port` is mandatory

- Usually `-host` **will not need to be specified** - it defaults machine you are running the code on.

- If the video does not have the right orientation - this can be fixed with `-rotate`.  It defaults to `0` (zero).  Common settings wil be `0`, `90`, `180`, `270`

**Example:**

1. Start `stream.py` and have it serve streaming video on port `8082` rotated `180` deg

    `python3 ./stream.py -port 8082 -rotate 180`
    
2. Browse to: `http://<ip-of-your-pi>:8082/stream.mjpg`


## Start stream.py during bootup
- `sudo nano /etc/rc.local`
- Above the line `exit 0`, add the following line:
  
    `/usr/bin/python3 /home/pi/stream.py -port 8082 -rotate 180`
  
    Assumptions made:
    - `which python3` prints `/usr/bin/python3`
    - You downloaded the stream.py script to the pi user home directory
    - You can also set the port param and rotation here as required
    - Adjust the paths accordingly should `python3` be installed somehwere else or you downloaded the script not your pi user home directory
- Save the changes
- `sudo reboot`

