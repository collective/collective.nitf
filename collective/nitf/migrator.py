# encoding: utf-8
import logging
import sys

logger = logging.getLogger('collective.nitf')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.debug(u'\nBegin collective.nitf LOG')

import transaction
from five import grok
from zope.component import createObject
from zope.component import queryUtility
from zope.component import queryMultiAdapter
from zope.event import notify
from zope.interface import classProvides
from zope.interface import implements
from zope.lifecycleevent import ObjectCreatedEvent
from zope.lifecycleevent import ObjectAddedEvent
from zope.lifecycleevent import ObjectModifiedEvent
from zope.schema import getFieldsInOrder

from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFPlone.utils import getToolByName, _createObjectByType
from plone.app.textfield.value import RichTextValue
from plone.dexterity.utils import createContentInContainer
from plone.dexterity.utils import iterSchemata
from plone.dexterity.interfaces import IDexterityFTI
from plone.uuid.interfaces import IMutableUUID
from z3c.form.interfaces import IValue

from collective.transmogrifier.interfaces import ISection, ISectionBlueprint
from collective.transmogrifier.transmogrifier import Transmogrifier

_marker = object()


class NITFTransformView(grok.View):
    grok.context(IPloneSiteRoot)
    grok.name(u'transform')
    def render(self):
        portal_state = queryMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        portal = portal_state.portal()
        self.transmogrify(portal)

        cat = getToolByName(portal, 'portal_catalog')
        cat.refreshCatalog(clear=False)
        logger.info('Catálogo principal actualizado')

        return 'Import terminado...'

    def transmogrify(self, context):
        self.transmogrifier = Transmogrifier(context)
        self.transmogrifier("nitfmigrator")

class CatalogNewsSource(object):
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


class NewsToNITFTransform(object):
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.context = transmogrifier.context
        self.previous = previous
        self.name = name

    def __iter__(self):
        for item in self.previous:
            item
        for item in self.previous:
            objct = item.getObject()
            parent = objct.__parent__
            o_id = item['id']
            n_id = o_id + '-old'
            parent.manage_renameObject(o_id, n_id)
            news_obj = parent[n_id]
            #parent[n_id] = objct
            #del parent[o_id]
            parent.invokeFactory('collective.nitf.content', id=o_id,
                                 )
            nitf_obj = parent[o_id]
            #fti = queryUtility(IDexterityFTI, name='collective.nitf.content')
            #factory = fti.factory
            #nitf_obj = createObject(factory)
            #get all fields for this obj
            for schemata in iterSchemata(nitf_obj):
                for name, field in getFieldsInOrder(schemata):
                    # FIXME creators field isn't setting at all.
                    #       problem with dexterity, apparently
                    #if name is 'creators':
                    #    continue
                    #setting value from the blueprint cue
                    if name == 'creators':
                        value = news_obj.Creators()
                        creator_list = []
                        for creator in value:
                            creator_list.append(unicode(creator))

                        value = tuple(creator_list)
                    else:
                        value = news_obj.get(name, _marker)
                    if value is _marker:
                        # No value is given from the pipeline,
                        # so we try to set the default value
                        # otherwise we set the missing value
                        default = queryMultiAdapter((
                                nitf_obj,
                                nitf_obj.REQUEST, # request
                                None, # form
                                field,
                                None, # Widget
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
                    field.set(field.interface(nitf_obj), value)
            nitf_obj.setTitle(u'%s' % news_obj.title)
            nitf_obj.setDescription(u'%s' % news_obj.Description())
            nitf_obj.setCreators(news_obj.creators)
            nitf_obj.body = RichTextValue(news_obj.getText(), 'text/html', 
                                          'text/x-html-safe')
            notify(ObjectCreatedEvent(nitf_obj))
            parent[nitf_obj.id] = nitf_obj
            parent[nitf_obj.id].reindexObject()
            yield parent[nitf_obj.id]#item


class NITFImageImport(object):
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
            logger.debug(u"\nObject: %s: Contained IDs :%s" %(nitf_obj,
                                                      nitf_obj.objectIds()))
            logger.debug(u"\t\tportal_type: %s title: %s description: %s creators: %s subject: %s" % (
                    nitf_obj.portal_type, nitf_obj.title, nitf_obj.description, nitf_obj.creators, nitf_obj.subject))
            logger.debug(u"\t\tDate Created: %s Date Modified: %s Expiration Date: %s Effective Date: %s" % (
                    nitf_obj.CreationDate(), nitf_obj.ModificationDate(),
                    nitf_obj.ExpirationDate(), nitf_obj.EffectiveDate()))
            if nitf_obj.objectIds():
                for objc in nitf_obj.objectIds():
                    logger.debug(u"%s" % nitf_obj[objc].tag())
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
                        obj.REQUEST, # request
                            None, # form
                            field,
                            None, # Widget
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

