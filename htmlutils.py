from HTMLParser import HTMLParser

class TagExtractor(HTMLParser):
    def __init__(self, hier, attrs):
        self._trg_hier = tuple(hier)
        self._trg_attrs = set((k,v) for k, v in attrs)
        self._stack = []
        self.found = None
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if self.found is not None:
            return
        self._stack.append(tag.lower())
        if tuple(self._stack) == self._trg_hier:
            if self._trg_attrs <= set(attrs):
                self.found = attrs
                #self.close()

    def handle_endtag(self, tag):
        if self.found is not None:
            return
        if self._stack:
            if self._stack[-1] == tag.lower():
                self._stack.pop()

if __name__ == '__main__':
    import sys
    text = sys.stdin.read()
    te = TagExtractor(['html','head','meta'], [('property', 'al:android:url')])
    te.feed(text)
    print te.found
