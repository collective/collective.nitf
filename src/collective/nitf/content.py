# -*- coding: utf-8 -*-
from collective.nitf import _
from collective.nitf.controlpanel import INITFSettings
from collective.z3cform.widgets.multicontent_search_widget import MultiContentSearchFieldWidget
from five import grok
from plone.app.dexterity.behaviors.metadata import IDublinCore
from plone.app.textfield import RichText
from plone.app.textfield.interfaces import ITransformer
from plone.dexterity.content import Container
from plone.directives import form
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.indexer import indexer
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import INonStructuralFolder
from z3c.relationfield.schema import RelationChoice, RelationList
from zope import schema
from zope.component import getUtility


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
        vocabulary=u'collective.nitf.AvailableSections',
        )

    urgency = schema.Choice(
        # nitf/head/docdata/urgency/@ed-urg
        title=_(u'Urgency'),
        description=_(u'help_urgency',
                      default=u'News importance.'),
        vocabulary=u'collective.nitf.Urgencies',
        )

    # XXX: this field uses a special widget that access the most recent items
    # of content types defined in the control panel; see browser.py and
    # controlpanel.py for more information
    relatedItems = RelationList(
        title=_(u'label_related_items', default=u'Related Items'),
        default=[],
        value_type=RelationChoice(title=u"Related",
                                  source=ObjPathSourceBinder()),
        required=False,
        )
    form.widget(relatedItems=MultiContentSearchFieldWidget)

    location = schema.TextLine(
        # nitf/body/body.head/dateline/location
        title=_(u'Location'),
        description=_(u'help_location',
                      default=u'Event location. Where an event took '
                               'place (as opposed to where the story was '
                               'written).'),
        required=False,
        )

    form.fieldset(
        'categorization',
        label=_(u'Categorization'),
        fields=['relatedItems', 'section', 'urgency', 'genre', 'subjects',
                'language'],
        )


class NITF(Container):
    grok.implements(INITF, INonStructuralFolder)


@form.default_value(field=INITF['genre'])
def genre_default_value(data):
    registry = getUtility(IRegistry)
    settings = registry.forInterface(INITFSettings)
    return settings.default_genre


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


# TODO: move this to Dexterity's core
@form.default_value(field=IDublinCore['language'])
def language_default_value(data):
    """ Returns portal's default language or None.
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
