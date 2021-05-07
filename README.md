# Pi-Camera-Streamer

This is a simple video streamer for use with the Pi Camera.  It streams video in mjpg format.
It is particularly useful when you want to same video feed to be consumed by more than one application.  For example a timelapse recording application and to also monitor in real time.


It is an adaptation of this work:
http://picamera.readthedocs.io/en/latest/recipes2.html#web-streaming

It was updated to use threadingHTTPServer and SimpleHTTPhandleror as well as allowing configuration from the command line

Its written using Python3

**Installation:**
Download to a directory of your choice.

`wget https://github.com/stuartofmt/Pi-Camera-Streamer/raw/main/stream.py  -O stream.py`

then make it executable

`chmod 744 stream.py`

**Startup:**

python3 stream.py -port [-host] [-rotate]

Specifying a port is mandatory.

Usually -host **will not need to be specified** - it defaults machine you are running the code on.

If the video does not have the right orientation - this can be fixed with -rotate.  It defaults to 0 (zero).  Common settings wil be 0, 90, 180, 270

**Example:**

Start stream.py and have it serve streaming video on port 8081 rotated 180 deg

`python3 ./stream.py -port 8082 -rotate 180`

