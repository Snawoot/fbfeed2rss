from lxml import etree
import datetime
from utctz import UTCTZ
from email.Utils import formatdate

epoch = datetime.datetime(1970,1,1, tzinfo = UTCTZ())

def to_rss_date(dt):
    return formatdate( (dt - epoch).total_seconds() )

class RSSItem:
    def __init__(self, link, title, description, pub_date = None, guid = None):
        self.title = title
        self.description = description
        self.link = link
        self.guid = guid
        if isinstance(pub_date, (datetime.datetime, type(None))):
            self.pub_date = pub_date
        else:
            raise TypeError('pub_date must be an instance of datetime or None')

class RSSFeed:
    def __init__(self, link = None, title = None, description = None, build_date = None):
        self._items = []
        self.title = title
        self.description = description
        self.link = link
        if isinstance(build_date, (datetime.datetime, type(None))):
            self.build_date = build_date
        else:
            raise TypeError('build_date must be an instance of datetime or None')

    def append_item(self, link, desc, title, pub_date = None, guid = None):
        self._items.append(RSSItem(link, desc, title, pub_date, guid))

    def marshal(self, f):
        feed = etree.Element('rss')
        feed.set('version', '2.0')

        channel = etree.Element('channel')
        feed.append(channel)

        if self.title is not None:
            title = etree.Element('title')
            title.text = self.title
            channel.append(title)

        if self.description is not None:
            description = etree.Element('description')
            description.text = self.description
            channel.append(description)

        if self.link is not None:
            link = etree.Element('link')
            link.text = self.link
            channel.append(link)

        if self.build_date is not None:
            build_date = etree.Element('lastBuildDate')
            build_date.text = to_rss_date(self.build_date)
            channel.append(build_date)

        for i in self._items:
            item = etree.Element('item')

            if i.title is not None:
                title = etree.Element('title')
                title.text = i.title
                item.append(title)

            if i.description is not None:
                description = etree.Element('description')
                description.text = i.description
                item.append(description)

            if i.link is not None:
                link = etree.Element('link')
                link.text = i.link
                item.append(link)

            if i.pub_date is not None:
                pub_date = etree.Element('pubDate')
                pub_date.text = to_rss_date(i.pub_date)
                item.append(pub_date)

            if i.guid is not None:
                guid = etree.Element('guid')
                guid.text = i.guid
                item.append(guid)
            channel.append(item)


        etree.ElementTree(feed).write(f, encoding='utf-8', xml_declaration=True) 
