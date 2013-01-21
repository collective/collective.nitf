# -*- coding: utf-8 -*-

from DateTime import DateTime

from zope.cachedescriptors.property import Lazy as lazy_property

from zope.component.hooks import getSite
from zope.component import queryMultiAdapter

from zope.interface import implementsOnly

from Products.CMFCore.utils import getToolByName

from collective.nitf.content import INITF
from collective.nitf.interfaces import INewsMLFeed
from collective.nitf.interfaces import INewsMLSyndicatable


class NewsMLFeed(object):
    implementsOnly(INewsMLFeed)

    def __init__(self, context):
        self.context = context
        syndication = getToolByName(self.context, 'portal_syndication')
        self.limit = syndication.max_items
        self.site = getSite()

    @lazy_property
    def site_url(self):
        return self.site.absolute_url()

    @property
    def logo(self):
        return '%s/logo.png' % self.site.absolute_url()

    @lazy_property
    def current_date(self):
        return DateTime()

    def _brains(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        return catalog(path={
            'query': '/'.join(self.context.getPhysicalPath()),
            'depth': 1
        })[:self.limit]

    def _items(self):
        """
        do catalog query
        """
        return [b.getObject() for b in self._brains()]

    @property
    def items(self):
        if INITF.providedBy(self.context):
            adapter = queryMultiAdapter((self.context, self), INewsMLSyndicatable)
            yield adapter
        else:
            for item in self._items():
                if INewsMLSyndicatable.providedBy(item):
                    adapter = queryMultiAdapter((item, self), INewsMLSyndicatable)
                    yield adapter
                else:
                    continue


class NewsMLCollectionFeed(NewsMLFeed):

    def _brains(self):
        return self.context.queryCatalog(batch=False)[:self.limit]
