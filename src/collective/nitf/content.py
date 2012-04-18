# -*- coding: utf-8 -*-

import unicodedata


from five import grok
from zope import schema
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary

from plone.app.dexterity.behaviors.metadata import IDublinCore
from plone.app.textfield import RichText
from plone.app.textfield.interfaces import ITransformer
from plone.directives import form
from plone.indexer import indexer
from plone.registry.interfaces import IRegistry

from Products.CMFCore.utils import getToolByName

from collective.nitf import _
from collective.nitf import config
from collective.nitf.controlpanel import INITFSettings


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

    #description = schema.Text()
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

    form.order_before(genre='subjects')
    genre = schema.Choice(
            # nitf/head/tobject/tobject.property/@tobject.property.type
            title=_(u'Genre'),
            description=_(u'help_genre',
                          default=u'Describes the nature, journalistic or '
                                   'intellectual characteristic of a news '
                                   'object, not specifically its content.'),
            source=u'collective.nitf.AvailableGenres',
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
            # nitf/body/body.head/dateline/location
            title=_(u'Location'),
            description=_(u'help_location',
                          default=u'Event location. Where an event took '
                                   'place (as opposed to where the story was '
                                   'written).'),
            required=False,
        )


@form.default_value(field=INITF['genre'])
def genre_default_value(data):
    registry = getUtility(IRegistry)
    settings = registry.forInterface(INITFSettings)
    return settings.default_genre


class AvailableGenresVocabulary(object):
    """Creates a vocabulary with the available genres stored in the registry; the
    vocabulary is normalized to allow the use of non-ascii characters.
    """
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(INITFSettings)
        items = []
        if settings.possible_genres:
            for genre in settings.possible_genres:
                token = unicodedata.normalize('NFKD', genre).encode('ascii', 'ignore').lower()
                items.append(SimpleVocabulary.createTerm(genre, token, _(genre)))
        return SimpleVocabulary(items)

grok.global_utility(AvailableGenresVocabulary, name=u'collective.nitf.AvailableGenres')


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


@form.default_value(field=IDublinCore['language'])
def language_default_value(data):
    """Returns portal's default language or English.
    """
    portal_properties = getToolByName(data, "portal_properties", None)
    if portal_properties is not None:
        site_properties = getattr(portal_properties, 'site_properties', None)
        if site_properties is not None:
            if site_properties.hasProperty('default_language'):
                return site_properties.getProperty('default_language')


@indexer(INITF)
def textIndexer(obj):
    """SearchableText contains id, title, subtitle, abstract, author and body
    text as plain text.
    """
    transformer = ITransformer(obj)

    result = u'%s %s' % (obj.id, obj.Title())

    if obj.subtitle:
        result += u' %s' % obj.subtitle

    if obj.Description():
        result += u' %s' % obj.Description()

    if obj.byline:
        result += u' %s' % obj.byline

    if obj.text:
        result += u' %s' % transformer(obj.text, 'text/plain')

    if obj.location:
        result += u' %s' % obj.location

    return result

grok.global_adapter(textIndexer, name='SearchableText')
