
from zope.component import getAdapter

from Products.Five import BrowserView

from collective.nitf.interfaces import INewsMLFeed


class NewsMLFeedView(BrowserView):

    def feed(self):
        return getAdapter(self.context, INewsMLFeed)
