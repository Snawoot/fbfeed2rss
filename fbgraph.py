import urllib2
import json

_feed_url = 'https://graph.facebook.com/%(ID)d/feed?access_token=%(access_token)s'
_group_url = 'https://graph.facebook.com/%(ID)d?access_token=%(access_token)s'

class FBGraph:
    def __init__(self, access_token, timeout=5):
        """ Init class with FB API access token """
        if isinstance(access_token, basestring):
            self._access_token = str(access_token)
            self._timeout = timeout
        else:
            raise TypeError("Access token should be a string")
    
    def get_group(self, group_id):
        requrl = _group_url % {
            'access_token': self._access_token,
            'ID': group_id
        }
        o = json.load(urllib2.urlopen(requrl, timeout = self._timeout))
        return o

    def get_feed(self, feed_id):
        requrl = _feed_url % {
            'access_token': self._access_token,
            'ID': feed_id
        }
        o = json.load(urllib2.urlopen(requrl, timeout = self._timeout))
        return o
