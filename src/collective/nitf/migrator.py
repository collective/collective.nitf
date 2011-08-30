# -*- coding: utf-8 -*-

import pprint
import zope.event

from five import grok
from plone.app.textfield.value import RichTextValue
from plone.uuid.interfaces import IMutableUUID
from zope.component import queryMultiAdapter
from zope.interface import classProvides
from zope.interface import implements
from zope.lifecycleevent import ObjectCreatedEvent
from zope.lifecycleevent import ObjectModifiedEvent

from Products.Archetypes.Field import Image
from Products.Archetypes.Schema import getNames
from Products.ATContentTypes.interfaces import IATNewsItem
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFPlone.utils import _createObjectByType
from Products.CMFPlone.utils import getToolByName

from collective.transmogrifier.interfaces import ISection, ISectionBlueprint
from collective.transmogrifier.transmogrifier import Transmogrifier

from collective.nitf.content import INITF
from collective.nitf.content import kind_default_value
from collective.nitf.content import section_default_value
from collective.nitf.content import urgency_default_value


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

        # set up new object id suffix using generateUniqueId script from Plone
        self.tmp = '-tmp.%s' % context.generateUniqueId()

    def __iter__(self):
        for item in self.previous:
            yield item

        for item in self.results:
            obj = item.getObject()
            path = '/'.join(obj.getPhysicalPath())

            schema = dict()
            schema['_type'] = 'collective.nitf.content'
            schema['_from'] = path  # we store here the original path
            schema['_path'] = path + self.tmp

            for name in getNames(obj.Schema()):
                field = obj.getField(name)
                schema[name] = field.get(obj)

            yield schema


class SchemaUpdater(object):
    """Update NITF schema.
    """
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous
        self.context = transmogrifier.context
        # TODO: implement options to set default values
        self.options = options

    def __iter__(self):
        for item in self.previous:

            path = item['_path']
            obj = self.context.unrestrictedTraverse(path, None)

            if not INITF.providedBy(obj):  # path does not exist or not a NITF
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
            # TODO: reimplement when relatedItems issue is solved
            #obj.relatedItems = item['relatedItems']
            obj.location = item['location']
            obj.setLanguage(item['language'])

            # Dates
            obj.setEffectiveDate(item['effectiveDate'])
            obj.setExpirationDate(item['expirationDate'])

            # Ownership
            obj.setCreators(item['creators'])
            obj.setContributors(item['contributors'])
            obj.setRights(item['rights'])

            zope.event.notify(ObjectModifiedEvent(obj))

            yield item


class ImageMigrator(object):
    """Converts the News Item image field into an ATImage.
    """
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous
        self.context = transmogrifier.context

    def __iter__(self):
        for item in self.previous:

            if not isinstance(item['image'], Image):  # no image or not an Image
                yield item; continue

            path = item['_path']
            container = self.context.unrestrictedTraverse(path, None)

            if not INITF.providedBy(container):  # path does not exist or not a NITF
                yield item; continue

            try:
                _createObjectByType('Image', container, 'image', title='image')
            except:
                # could not create image
                yield item; continue

            image = container['image']
            image.setDescription(item['imageCaption'])
            image.setImage(item['image'])

            zope.event.notify(ObjectCreatedEvent(image))

            yield item


class ReplaceObject(object):
    """Deletes News Items and renames NITF news articles using its ids;
    assures link integrity by reusing original UUID.
    """
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous
        self.context = transmogrifier.context

    def __iter__(self):
        for item in self.previous:

            path = item['_path']
            nitf = self.context.unrestrictedTraverse(path, None)

            if not INITF.providedBy(nitf):  # path does not exist or not a NITF
                yield item; continue

            path = item['_from']
            newsitem = self.context.unrestrictedTraverse(path, None)

            if not IATNewsItem.providedBy(newsitem):  # path does not exist or not a News Item
                yield item; continue

            # delete News Item and replace NITF UUID to assure link integrity
            id = newsitem.getId()
            uuid = newsitem.UID()
            folder = newsitem.aq_parent
            # FIXME: this seems to be trigering manage_beforeDelete in
            # Archetypes/Referenceable.py removing News Item object references
            # before we replace them with the new NITF news article object
            folder.manage_delObjects([id])
            folder.manage_renameObject(nitf.getId(), id)
            IMutableUUID(nitf).set(uuid)

            zope.event.notify(ObjectModifiedEvent(nitf))

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
