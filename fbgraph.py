import urllib
import urllib2
import json

_feed_url = 'https://graph.facebook.com/v2.6/%(ID)d/feed?access_token=%(access_token)s&limit=%(limit)d'
_group_url = 'https://graph.facebook.com/v2.6/%(ID)d?access_token=%(access_token)s'

class FBGraph:
    def __init__(self, access_token, timeout=5):
        """ Init class with FB API access token """
        if isinstance(access_token, basestring):
            self._access_token = str(access_token)
            self._timeout = timeout

            app_id, _, app_token = self._access_token.partition('|')
            self._app_id = int(app_id) if app_token else None
        else:
            raise TypeError("Access token should be a string")
    
    def get_group(self, group_id):
        requrl = _group_url % {
            'access_token': self._access_token,
            'ID': group_id
        }
        o = json.load(urllib2.urlopen(requrl, timeout = self._timeout))
        return o

    def get_feed(self, feed_id, limit=25, continue_url = None):
        requrl = _feed_url % {
            'access_token': self._access_token,
            'ID': feed_id,
            'limit': limit
        } if continue_url is None else continue_url
        o = json.load(urllib2.urlopen(requrl, timeout = self._timeout))
        return o

    def create_user(self):
        if self.app_id is None:
            raise ValueError('Unable to create user with Graph API instance initizized with page or user access token')
        else:
            return fbuser.FBUser(
                self._access_token,
                self._app_id,
                self._timeout
            )

