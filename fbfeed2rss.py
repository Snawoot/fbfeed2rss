#!/usr/bin/python
import BaseHTTPServer
import SocketServer
import gatehandler
import argparse

default_host = '0.0.0.0'
default_port = 1716

class ThreadedHTTPServer(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer):
    """Handle requests in a separate thread."""

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Facebook feed API to RSS gate')
    parser.add_argument('-H', '--host', metavar='ADDRESS',
        help='listen address (default: %s)' % (repr(default_host),), default=default_host)
    parser.add_argument('-p', '--port', metavar='PORT',
        help='listen port (default: %s)' % (repr(default_port),), type=int, default=default_port)
    args = parser.parse_args()

    server = ThreadedHTTPServer((args.host, args.port), gatehandler.GateHandler)
    server.serve_forever()
