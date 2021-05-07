# Web streaming
# Source code from the official PiCamera package
# http://picamera.readthedocs.io/en/latest/recipes2.html#web-streaming

# Modified by Stuartofmt
# Released under The MIT License. Full text available via https://opensource.org/licenses/MIT
# Updated to use threadingHTTPServer and SimpleHTTPhandler

import argparse
import io
import picamera
import logging
# import socketserver
from threading import Condition
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer


streamVersion = '1.0.0'


def init():
    # parse command line arguments
    parser = argparse.ArgumentParser(
            description='Streaming http server for Pi camera. V' + streamVersion,
            allow_abbrev=False)
    # Environment
    parser.add_argument('-host', type=str, nargs=1, default=['0.0.0.0'],
                        help='The ip address this service listens on. Default = 0.0.0.0')
    parser.add_argument('-port', type=int, nargs=1, default=[0],
                        help='Specify the port on which the server listens. Default = 0')
    parser.add_argument('-rotate', type=str, nargs=1, default=['0'], help='Rotation. Default = 0')
    args = vars(parser.parse_args())

    global host, port, rotate

    host = args['host'][0]
    port = args['port'][0]
    rotate = args['rotate'][0]


class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)


class StreamingHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        print(self.path)
        if self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', '0')
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    try:
                        self.wfile.write(b'--FRAME\r\n')
                        self.send_header('Content-Type', 'image/jpeg')
                        self.send_header('Content-Length', str(len(frame)))
                        self.end_headers()
                        self.wfile.write(frame)
                        self.wfile.write(b'\r\n')
                    except:
                        print('Client Disconnected')
                        break
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))

        else:
            self.send_error(404)
            self.end_headers()


"""
Main Program
"""


if __name__ == "__main__":
    global host, port, rotate
    init()

    with picamera.PiCamera(resolution='1024x768', framerate=24) as camera:
        output = StreamingOutput()
        camera.rotation = rotate
        camera.start_recording(output, format='mjpeg')
        try:
            server = ThreadingHTTPServer((host, port), StreamingHandler)
            server.serve_forever()
        finally:
            camera.stop_recording()
