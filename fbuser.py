import urllib
import urllib2
import json

_test_users_url = 'https://graph.facebook.com/v2.6/%(app_id)d/accounts/test-users?access_token=%(access_token)'
_user_url = 'https://graph.facebook.com/v2.6/%(ID)d?access_token=%(access_token)s'

_fb_url = 'https://facebook.com/'
_fblogin_url = 'https://www.facebook.com/login.php?login_attempt=1'

class FBUser:
    def __init__(self, access_token, app_id, timeout=5):
        """Create test user via FB Application API"""
        self._timeout = timeout

        if isinstance(access_token, basestring):
            self._access_token = str(access_token)
        else:
            raise TypeError("Access token should be a string")

        if isinstance(app_id, (int,long)):
            self._app_id = app_id
        else:
            raise TypeError("App ID should be an integer number")

        self.uid = None
        self.uid, self.email, self.passwd = self._create_uid()
        self.session = self._auth_session()

    def _create_uid(self):
        requrl = _test_users_url % {
            'access_token': self._access_token,
            'app_id': self._app_id
        }
        o = json.load(urllib2.urlopen(requrl, data='', timeout = self._timeout))
        return o['id'], o['email'], o['password']

    def _eliminate_uid(self):
        requrl = _user_url % {
            'access_token': self._access_token,
            'ID': self.uid
        }
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        request = urllib2.Request(requrl)
        request.get_method = lambda: 'DELETE'
        o = json.load(opener.open(request, timeout = self._timeout))
        if not o['success']:
            raise Exception('FBUser uid=%d: elimination failed!' % (self.uid,))

    def _auth_session(self):
        cj = CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        opener.open(_fb_url).read()
        formdata = urllib.urlencode(
            {
                'email': email,
                'pass': passwd,
                'persistent':'',
                'default_persistent': 1
            }
        )
        opener.open(_fblogin_url, formdata).read()
        return cj

    def fetch_url(self, *args):
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.session))
        return opener.open(*args).read()

    def __del__(self):
        if self.uid is not None:
            self._eliminate_uid()

