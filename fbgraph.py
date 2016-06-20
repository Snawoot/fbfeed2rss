import urllib2

_feed_url = 'https://graph.facebook.com/%(ID)d/feed?access_token=%(access_token)s'

class FBGraph:
    def __init__(self, token, timeout=5):
        """ Init class with FB API access token """
        if isinstance(key, basestring):
            self._token = str(token)
            self._timeout = timeout
        else:
            raise TypeError("Access token should be a string")
    
    def get_feed(self, feed_id):
        requrl = _feed_url % {
            'access_token': self.token,
            'ID': feed_id
        }
        return urllib2.urlopen(requrl, timeout = self._timeout)
