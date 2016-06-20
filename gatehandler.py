import BaseHTTPServer
import handlerutils

class GateHandler(BaseHTTPServer.BaseHTTPRequestHandler,
    handlerutils.HandlerUtilsMixIn):
    def r_hello(self):
        """ Test route """
        self.finalize('Hello World!\n',
            headers = (('Content-Type', 'text/plain'),))

    def r_feed(self):
        pass
        
    routes = {
        '/rss/v1.0/hello': r_hello,
        '/rss/v1.0/feed': r_feed,
    }

    def do_GET(self):
        self.route(self.routes)
