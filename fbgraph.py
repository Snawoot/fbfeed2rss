import urllib2

class FBGraph:
    def __init__(self, token):
        """ Init class with FB API access token """
        if isinstance(key, basestring):
            self._token = str(token)
        else:
            raise TypeError("Access token should be a string")
