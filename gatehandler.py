import BaseHTTPServer
import urlparse
import posixpath

class GateHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def r_hello(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write('Hello World!\n')
        
    routes = {
        '/rss/v1.0/hello': r_hello,
    }

    def do_GET(self):
        path = urlparse.urlparse(self.path).path
        normpath = posixpath.normpath(path)
        if normpath in self.routes:
            self.routes[normpath](self)
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write('Request %s is unsupported!\n' % (repr(normpath),))

