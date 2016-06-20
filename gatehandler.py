import BaseHTTPServer
import handlerutils

class GateHandler(BaseHTTPServer.BaseHTTPRequestHandler,
    handlerutils.HandlerUtilsMixIn):
    def __init__(self, request, client_address, server, env):
        self.env = env
        BaseHTTPServer.BaseHTTPRequestHandler.__init__(self,
            request, client_address, server)
    def r_hello(self):
        """ Test route """
        self.finalize('Hello World!\n',
            headers = (('Content-Type', 'text/plain'),))

    def r_feed(self):
        args = self.get_args()
        if 'id' not in args:
            self.send_error(400, 'Missing required query parameter: id')
            return

        try:
            ID = int(args['id'])
        except:
            self.send_error(400, 'Unable to parse integer parameter: id')
            return
        self.finalize(repr(self.env['key']))
        
    routes = {
        '/rss/v1.0/hello': r_hello,
        '/rss/v1.0/feed': r_feed,
    }

    def do_GET(self):
        self.route(self.routes)
