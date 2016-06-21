from datetime import tzinfo, timedelta, datetime

ZERO = timedelta(0)

class UTCTZ(tzinfo):
    """UTC"""

    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    name = tzname

    def dst(self, dt):
        return ZERO
