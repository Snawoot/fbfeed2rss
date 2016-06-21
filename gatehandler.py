import BaseHTTPServer
import handlerutils
import rssfeed
import datetime
import iso8601
import textwrap
from utctz import UTCTZ

_rss_mime_type = 'text/xml'

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
        if self.command == 'HEAD':
            self.finalize(headers = (('Content-Type', _rss_mime_type),))
            return

        args = self.get_args()
        if 'id' not in args:
            self.send_error(400, 'Missing required query parameter: id')
            return

        try:
            ID = int(args['id'])
        except:
            self.send_error(400, 'Unable to parse integer parameter: id')
            return

        try:
            feedobj = self.env.graphapi.get_feed(ID, limit=100)
        except:
            self.send_error(500, 'Unable to fetch feed')
            return
            
        try:
            groupobj = self.env.graphapi.get_group(ID)
            groupname = groupobj['name']
        except:
            groupname = 'Facebook feed %d' % (ID,)
            
        feed = rssfeed.RSSFeed(
            'https://facebook.com/%s' % (ID,),
            groupname,
            groupname,
            datetime.datetime.now(UTCTZ())
        )
        
        for post in feedobj['data']:
            posturl = 'https://facebook.com/' + post['id']
            feed.append_item(posturl,
                textwrap.wrap(post['message'])[0] + '...' if 'message' in post else post.get('story') or post['id'],
                post['message'] if 'message' in post else post.get('story', '') + ':' + posturl,
                iso8601.parse_date(post['updated_time']),
                post['id']
            )

        self.send_response(200)
        self.send_header('Content-Type', _rss_mime_type)
        self.send_header('Connection', 'close')
        self.end_headers()
        feed.marshal(self.wfile)

    def r_icon(self):
        self.send_error(404)
        
    routes = {
        '/rss/v1.0/hello': r_hello,
        '/rss/v1.0/feed': r_feed,
        '/favicon.ico': r_icon
    }

    def do_GET(self):
        self.route(self.routes)
