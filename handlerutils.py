import urlparse
import posixpath
import os.path
import mimetypes

class HandlerUtilsMixIn:
    def finalize(self, body = None, code = 200, errmsg = None, headers = []):
        """ Utility function which covers full HTTP response cycle
        for given code, body and headers """
        self.send_response(code, errmsg)
        for h,v in headers:
            self.send_header(h, v)
        self.end_headers()
        if body is not None:
            self.wfile.write(body)

    def route(self, routes):
        """ Normalizes request path and passes
        request to an appropriate route handler """
        path = urlparse.urlparse(self.path).path
        normpath = posixpath.normpath(path)
        if normpath in routes:
            routes[normpath](self)
        else:
            self.send_error(400,
                'Route %s is unsupported!\n' % (repr(normpath),))

    def get_args(self):
        """ Get query string params """
        qs = urlparse.urlparse(self.path).query
        args = urlparse.parse_qs(qs)
        args = dict( (k, v[0]) for k, v in args.iteritems() )
        return args

    def serve_static(self, filename, mimetype = None):
        if mimetype is None:
            mimetype = mimetypes.guess_type(filename)[0]
        path = os.path.join(self.env.approot, filename)
        with open(path) as f:
            content = f.read()
        self.finalize(content,
            headers = (('Content-Type', mimetype),))
