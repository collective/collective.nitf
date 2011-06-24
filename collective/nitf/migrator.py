# encoding: utf-8
from zope.interface import classProvides
from zope.interface import implements

from Products.CMFPlone.utils import getToolByName

from collective.transmogrifier.interfaces import ISection, ISectionBlueprint


class NewsReader(object):
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.context = transmogrifier.context
        self.catalog = getToolByName(self.context, 'portal_catalog')
        self.results = self.catalog({'Type': 'News Item',},)
        self.previous = previous
        self.name = name

    def __iter__(self):
        for item in self.previous:
            yield item

        for res in self.results:
            yield res


class NITFTransform(object):
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.context = transmogrifier.context
        self.previous = previous
        self.name = name

    def __iter__(self):
        for item in self.previous:
            yield item

