# encoding: utf-8
import transaction
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
        for result in self.results:
            yield result


class NITFTransform(object):
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.context = transmogrifier.context
        self.previous = previous
        self.name = name

    def __iter__(self):
        for item in self.previous:
            objct = item.getObject()
            parent = objct.__parent__
            print item.getPath(), parent
            o_id = item['id']
            n_id = o_id + '-old'
            parent[n_id] = objct
            del parent[o_id]
            print o_id
            parent.invokeFactory('collective.nitf.content', id=o_id, title=item["Title"])
            del parent[n_id]
            item = parent[o_id]
            item.reindexObject()
            print item.id, item.Type()
            yield item

