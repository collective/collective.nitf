# -*- coding: utf-8 -*-

import unicodedata

from five import grok
from zope import schema
from zope.component import getUtility
from zope.interface import alsoProvides
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary

from Products.ATContentTypes.interfaces import IImageContent
from Products.CMFDefault.formlib.schema import SchemaAdapterBase

from plone.app.textfield import RichText
from plone.app.textfield.interfaces import ITransformer
from plone.directives import form
from plone.indexer import indexer
from plone.registry.interfaces import IRegistry

from collective.nitf import _
from collective.nitf import config
from collective.nitf.controlpanel import INITFSettings

VIDEO_MIMETYPES = ['video/mp4', 'video/x-flv']
IMAGE_MIMETYPES = ['image/jpeg', 'image/gif', 'image/png']


class INITF(form.Schema):
    """A news item based on the News Industry Text Format specification.
    """

    #title = schema.TextLine()
        # nitf/head/title and nitf/body/body.head/hedline/hl1

    form.order_after(subtitle='IDublinCore.title')
    subtitle = schema.TextLine(
            # nitf/body/body.head/hedline/hl2
            title=_(u'Subtitle'),
            description=_(u'help_subtitle',
                          default=u'A subordinate headline for the article.'),
            required=False,
            default=u'',
        )

    #abstract = schema.TextLine()
        # nitf/body/body.head/abstract

    byline = schema.TextLine(
            # nitf/body/body.head/byline/person
            title=_(u'Author'),
            required=False,
            default=u'',
        )

    text = RichText(
            # nitf/body/body.content
            title=_(u'Body text'),
            required=False,
        )

    kind = schema.Choice(
            # nitf/head/tobject/tobject.property/@tobject.property.type
            title=_(u'News Type'),
            vocabulary=config.NEWS_TYPES,
        )

    section = schema.Choice(
            # nitf/head/pubdata/@position.section
            title=_(u'Section'),
            description=_(u'help_section',
                          default=u'Named section where the article will '
                                   'appear.'),
            vocabulary=u'collective.nitf.Sections',
        )

    urgency = schema.Choice(
            # nitf/head/docdata/urgency/@ed-urg
            title=_(u'Urgency'),
            description=_(u'help_urgency',
                          default=u'News importance.'),
            vocabulary=config.URGENCIES,
        )

    form.order_after(location='IRelatedItems.relatedItems')
    location = schema.TextLine(
            # nitf/head/docdata/evloc
            title=_(u'Location'),
            description=_(u'help_location',
                          default=u'Event location. Where an event took '
                                   'place (as opposed to where the story was '
                                   'written).'),
            required=False,
        )


@form.default_value(field=INITF['kind'])
def kind_default_value(data):
    registry = getUtility(IRegistry)
    settings = registry.forInterface(INITFSettings)
    return settings.default_kind


class ImageContentAdapter(SchemaAdapterBase, grok.Adapter):
    grok.context(INITF)
    grok.provides(IImageContent)

    def __init__(self, context):
        super(ImageContentAdapter, self).__init__(context)
        self.context = context

    def getImage(self):
        img = None
        if len(self.context.objectIds()):
            return self.context[self.context.objectIds()[0]]
        return

    def setImage(self):
        return

    def tag(self):
        return

alsoProvides(INITF, IImageContent)


class SectionsVocabulary(object):
    """Creates a vocabulary with the sections stored in the registry; the
    vocabulary is normalized to allow the use of non-ascii characters.
    """
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(INITFSettings)
        items = []
        for section in settings.sections:
            token = unicodedata.normalize('NFKD', section).encode('ascii', 'ignore').lower()
            items.append(SimpleVocabulary.createTerm(section, token, section))
        return SimpleVocabulary(items)

grok.global_utility(SectionsVocabulary, name=u'collective.nitf.Sections')


@form.default_value(field=INITF['section'])
def section_default_value(data):
    registry = getUtility(IRegistry)
    settings = registry.forInterface(INITFSettings)
    return settings.default_section


@form.default_value(field=INITF['urgency'])
def urgency_default_value(data):
    registry = getUtility(IRegistry)
    settings = registry.forInterface(INITFSettings)
    return settings.default_urgency


@indexer(INITF)
def textIndexer(obj):
    """SearchableText contains id, title, subtitle, abstract, author and body
    text as plain text.
    """
    transformer = ITransformer(obj)
    text = transformer(obj.text, 'text/plain')
    return '%s %s %s %s %s %s %s' % (obj.id,
                                     obj.Title(),
                                     obj.subtitle,
                                     obj.Description(),
                                     obj.byline,
                                     text,
                                     obj.location)
grok.global_adapter(textIndexer, name='SearchableText')
