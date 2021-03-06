#!/usr/bin/python
import sys
import BaseHTTPServer
import SocketServer
import gatehandler
import argparse
import fbgraph
import os.path

default_host = '0.0.0.0'
default_port = 1716
default_keypath = 'fbtoken.txt'

class ThreadedHTTPServer(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer):
    """Handle requests in a separate thread."""
    request_queue_size = 50
    daemon_threads = True

    def __init__(self, server_address, RequestHandlerClass, env):
        """Pass additional variable when instantiating
        Request Handler class"""
        self._env = env
        BaseHTTPServer.HTTPServer.__init__(self, server_address, RequestHandlerClass)

    def finish_request(self, request, client_address):
        """Finish one request by instantiating RequestHandlerClass.
        This method is overriden here for passing additional
        environment parameter"""
        self.RequestHandlerClass(request, client_address, self, self._env)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Facebook feed API to RSS gate')
    parser.add_argument('-H', '--host', metavar='ADDRESS',
        help='listen address (default: %s)' % (repr(default_host),), default=default_host)
    parser.add_argument('-p', '--port', metavar='PORT',
        help='listen port (default: %s)' % (repr(default_port),), type=int, default=default_port)
    parser.add_argument('-k', '--token-file', metavar='KEYFILE',
        help='path to application access token (text file containing facebook API access token, default: %s)' % (repr(default_keypath),),
        default=default_keypath)
    args = parser.parse_args()

    with open(args.token_file) as kf:
        key = kf.read().strip()
    if not key:
        raise ValueError("Key file is empty!")

    app_root = os.path.dirname(os.path.realpath(__file__))
    ga = fbgraph.FBGraph(key)
    print >> sys.stderr, "Creating FB test user account via FB Graph API. Please wait..."
    with ga.create_user() as fbuser:
        print >> sys.stderr, "Done."
        environ = type('Environment', (object,), { "graphapi": ga, "fbuser": fbuser, 'approot': app_root})

        server = ThreadedHTTPServer((args.host, args.port), gatehandler.GateHandler, environ)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print >> sys.stderr, "Stoping and cleaning up..."
    print >> sys.stderr, "Cleanup complete."
