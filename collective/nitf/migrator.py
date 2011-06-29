# encoding: utf-8
import transaction
from zope.component import queryMultiAdapter
from zope.event import notify
from zope.interface import classProvides
from zope.interface import implements
from zope.lifecycleevent import ObjectAddedEvent
from zope.lifecycleevent import ObjectModifiedEvent
from zope.schema import getFieldsInOrder

from Products.CMFPlone.utils import getToolByName
from plone.app.textfield.value import RichTextValue
from plone.dexterity.utils import iterSchemata
from plone.uuid.interfaces import IMutableUUID
from z3c.form.interfaces import IValue

from collective.transmogrifier.interfaces import ISection, ISectionBlueprint

_marker = object()


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
            o_id = item['id']
            n_id = o_id + '-old'
            parent.manage_renameObject(o_id, n_id)
            news_obj = parent[n_id]
            #parent[n_id] = objct
            #del parent[o_id]
            parent.invokeFactory('collective.nitf.content', id=o_id,
                                 )
            nitf_obj = parent[o_id]
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
            if news_obj.getImage():
                file_id = '.'.join(['image',
                                   news_obj.getImage().getContentType()[-3:]])
                # FIXME debugging lines
                #print file_id
                nitf_obj.invokeFactory('Image', id=file_id,
                                        title=news_obj.getImageCaption(),
                                        image=news_obj.getRawImage())
                notify(ObjectAddedEvent(nitf_obj))
            notify(ObjectModifiedEvent(nitf_obj))
            # FIXME debugging lines
            #print nitf_obj.Type(), nitf_obj.Title(), nitf_obj.Description(),
            #        nitf_obj.creators, nitf_obj.body.raw, nitf_obj.body.output
            del parent[n_id]
            yield item
