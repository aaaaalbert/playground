# Adapted from http://stackoverflow.com/questions/10017859/how-to-build-a-simple-http-post-server
# Thank you!

import sys
import BaseHTTPServer
import cgi

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        postvars = {}
        try:
          if ctype == 'application/x-www-form-urlencoded':
              length = int(self.headers.getheader('content-length'))
              postvars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
              print "Client posted", postvars

          self.send_response(200)
          """
          self.send_header("Content-type", "text")
          self.send_header("Content-length", str(len(body))) """
          self.end_headers()
          # self.wfile.write(body)
        except Exception, e:
          print "Error", repr(e)


def httpd(handler_class=MyHandler, server_address = ('127.0.0.1', 8000)):
    try:
        print "Server started"
        srvr = BaseHTTPServer.HTTPServer(server_address, handler_class)
        srvr.serve_forever() # serve_forever
    except KeyboardInterrupt:
        srvr.socket.close()


if __name__ == "__main__":
    httpd(server_address = (sys.argv[1], int(sys.argv[2])))

