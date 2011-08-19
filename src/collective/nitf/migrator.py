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
from zope.schema import getFieldsInOrder

from Products.Archetypes.Schema import getNames
from Products.ATContentTypes.interfaces import IATNewsItem
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFPlone.utils import getToolByName
from plone.app.textfield.value import RichTextValue
from plone.dexterity.utils import iterSchemata
from plone.dexterity.interfaces import IDexterityFTI
from z3c.form.interfaces import IValue

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
            obj = self.context.unrestrictedTraverse(path)
            newsitem = self.context.unrestrictedTraverse(path.partition('-tmp')[0])

            if not INITF.providedBy(obj):  # not a NITF
                yield item; continue

            if not IATNewsItem.providedBy(newsitem):  # not a News Item
                yield item; continue

            #obj.id = newsitem.getId()
            obj.title = newsitem.Title()
            obj.subtitle = ''
            obj.description = newsitem.Description()
            #obj.abstract = newsitem.Description()
            obj.byline = ''
            #obj.text = newsitem.getText()
            obj.kind = kind_default_value(None)
            obj.section = section_default_value(None)
            obj.urgency = urgency_default_value(None)
            obj.location = newsitem.getLocation()

            obj.subject = newsitem.Subject()
            obj.rights = newsitem.Rights()
            #obj.relatedItems = newsitem.getRelatedItems()
            obj.language = newsitem.Language()
            obj.modification_date = newsitem.ModificationDate()
            obj.contributors = newsitem.Contributors()
            #obj.creation_date = newsitem.CreationDate()
            obj.creators = newsitem.Creators()
            obj.effectiveDate = newsitem.getEffectiveDate()
            obj.excludeFromNav = newsitem.getExcludeFromNav()
            obj.expirationDate = newsitem.getExpirationDate()

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

    def setFieldsDefaults(self, obj, base_obj):
        for schemata in iterSchemata(obj):
            for name, field in getFieldsInOrder(schemata):
                # FIXME creators field isn't setting at all.
                #       problem with dexterity, apparently
                #setting value from the blueprint cue
                if name == 'creators':
                    value = base_obj.Creators()
                    creator_list = []
                    for creator in value:
                        creator_list.append(unicode(creator))

                    value = tuple(creator_list)
                else:
                    value = base_obj.get(self.name, _marker)
                if value is _marker:
                    # No value is given from the pipeline,
                    # so we try to set the default value
                    # otherwise we set the missing value
                    default = queryMultiAdapter((
                        obj,
                        obj.REQUEST,  # request
                            None,  # form
                            field,
                            None,  # Widget
                            ), IValue, name='default')
                    if default is not None:
                        default = default.get()
                    if default is None:
                        default = getattr(field, 'default', None)
                    if default is None:
                        try:
                            default = field.missing_value
                        except AttributeError:
                            pass
                    value = default
                field.set(field.interface(obj), value)


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
