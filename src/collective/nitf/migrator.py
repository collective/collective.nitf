# -*- coding: utf-8 -*-

import pprint

from five import grok
from zope.component import createObject
from zope.component import queryUtility
from zope.component import queryMultiAdapter
from zope.event import notify
from zope.interface import classProvides
from zope.interface import implements
from zope.lifecycleevent import ObjectAddedEvent
from zope.lifecycleevent import ObjectModifiedEvent

from Products.Archetypes.Schema import getNames
from Products.ATContentTypes.interfaces import IATNewsItem
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFPlone.utils import getToolByName
from plone.app.textfield.value import RichTextValue
from plone.dexterity.interfaces import IDexterityFTI

from collective.transmogrifier.interfaces import ISection, ISectionBlueprint
from collective.transmogrifier.transmogrifier import Transmogrifier

from collective.nitf.content import INITF
from collective.nitf.content import kind_default_value
from collective.nitf.content import section_default_value
from collective.nitf.content import urgency_default_value

_marker = object()


class NITFTransformView(grok.View):
    grok.context(IPloneSiteRoot)
    grok.name('nitf-migrator')

    def render(self):
        portal_state = queryMultiAdapter((self.context, self.request),
                                         name=u'plone_portal_state')
        portal = portal_state.portal()
        self.transmogrify(portal)

        return 'Migration finished...'

    def transmogrify(self, context):
        self.transmogrifier = Transmogrifier(context)
        self.transmogrifier("nitfmigrator")


class NewsItemSource(object):
    """Returns an iterator of objects from the catalog that implement
    IATNewsItem.
    """
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous

        context = transmogrifier.context
        catalog = getToolByName(context, 'portal_catalog')
        self.results = catalog(object_provides=IATNewsItem.__identifier__,
                               path='/'.join(context.getPhysicalPath()))

    def __iter__(self):
        for item in self.previous:
            yield item

        for item in self.results:
            obj = item.getObject()
            path = '/'.join(obj.getPhysicalPath())

            schema = dict()
            schema['_type'] = 'collective.nitf.content'
            schema['_path'] = '%s-tmp' % path

            for name in getNames(obj.Schema()):
                field = obj.getField(name)
                schema[name] = field.get(obj)

            yield schema


class SchemaUpdater(object):
    """Update NITF schema as transmogrify.dexterity is not ready.
    """
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous
        self.context = transmogrifier.context
        self.options = options

    def __iter__(self):
        for item in self.previous:

            path = item['_path']
            obj = self.context.unrestrictedTraverse(path, None)

            if not obj:  # path does not exist
                yield item; continue

            if not INITF.providedBy(obj):  # not a NITF
                yield item; continue

            # Content
            obj.title = item['title']
            obj.subtitle = ''
            obj.description = item['description']
            #obj.abstract = item['description']
            obj.byline = ''
            obj.text = RichTextValue(item['text'], 'text/html', 'text/x-html-safe')
            obj.kind = kind_default_value(None)
            obj.section = section_default_value(None)
            obj.urgency = urgency_default_value(None)

            # Categorization
            obj.setSubject(item['subject'])
            # TODO: solve relatedItems issue
            #obj.relatedItems = item['relatedItems']?
            obj.location = item['location']
            obj.setLanguage(item['language'])

            # Dates
            obj.setEffectiveDate(item['effectiveDate'])
            obj.setExpirationDate(item['expirationDate'])

            # Ownership
            obj.setCreators(item['creators'])
            obj.setContributors(item['contributors'])
            obj.setRights(item['rights'])

            obj.reindexObject()
            notify(ObjectModifiedEvent(obj))

            yield item


class NITFImageImport(object):
    # image, imageCaption
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous

    def __iter__(self):
        for item in self.previous:
            objct = item.getObject()
            parent = objct.__parent__
            o_id = item['id']
            n_id = o_id + '-old'
            parent[n_id] = objct
            news_obj = parent[n_id]
            news_obj.reindexObject()
            #parent[n_id] = objct
            del parent[o_id]
            #createContentInContainer(parent, 'collective.nitf.content', id=o_id, checkConstraints=False)
            #parent.invokeFactory('collective.nitf.content', id=o_id,
            #                     )
            fti = queryUtility(IDexterityFTI, name='collective.nitf.content')
            factory = fti.factory
            new_object = createObject(factory, id=o_id)
            #parent[o_id] = new_object

            #nitf_obj = parent[o_id]
            nitf_obj = new_object
            self.setFieldsDefaults(nitf_obj, news_obj)
            #get all fields for this obj
            nitf_obj.setTitle(u'%s' % news_obj.title)
            nitf_obj.setDescription(u'%s' % news_obj.Description())
            nitf_obj.setCreators(news_obj.creators)
            nitf_obj.setSubject(news_obj.Subject())
            nitf_obj.body = RichTextValue(news_obj.getText(), 'text/html',
                                          'text/x-html-safe')
            parent[o_id] = nitf_obj
            nitf_obj = parent[o_id]
            notify(ObjectAddedEvent(parent[o_id]))
            if news_obj.getImage():
                file_id = '.'.join(['image',
                                   news_obj.getImage().getContentType()[-3:]])
                # FIXME debugging lines
                #print file_id
                #_createObjectByType('Image', nitf_obj, id=file_id,
                nitf_obj.invokeFactory('Image', id=file_id,
                                        title=news_obj.getImageCaption(),
                                        image=news_obj.getRawImage())
            notify(ObjectModifiedEvent(parent[o_id]))
            parent[o_id].reindexObject()
            # FIXME debugging lines
            #print nitf_obj.Type(), nitf_obj.Title(), nitf_obj.Description(),
            #        nitf_obj.creators, nitf_obj.body.raw, nitf_obj.body.output
            del parent[n_id]
            yield item


class PrettyPrinter(object):
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous
        self.pprint = pprint.PrettyPrinter().pprint

    def __iter__(self):
        for item in self.previous:
            self.pprint(sorted(item.items()))
            yield item
