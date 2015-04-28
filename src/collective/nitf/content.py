# -*- coding: utf-8 -*-

from collective.nitf import _
from collective.nitf.controlpanel import INITFSettings
from collective.z3cform.widgets.multicontent_search_widget import MultiContentSearchFieldWidget
from five import grok
from plone.app.textfield import RichText
from plone.app.textfield.interfaces import ITransformer
from plone.dexterity.content import Container
from plone.app.dexterity.behaviors.metadata import IDublinCore
from plone.directives import form
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.indexer import indexer
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.component import getUtility


class INITF(form.Schema):
    """A news item based on the News Industry Text Format specification.
    """

    # title = schema.TextLine()
    # nitf/head/title and nitf/body/body.head/hedline/hl1

    form.order_after(subtitle='IDublinCore.title')
    subtitle = schema.TextLine(
        # nitf/body/body.head/hedline/hl2
        title=_(u'Subtitle'),
        description=_(u'help_subtitle',
                      default=u'A subordinate headline for the article.'),
        default=u'',
        missing_value=u'',
        required=False,
    )

    # description = schema.Text()
    # nitf/body/body.head/abstract

    byline = schema.TextLine(
        # nitf/body/body.head/byline/person
        title=_(u'Author'),
        default=u'',
        missing_value=u'',
        required=False,
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
                              u'intellectual characteristic of a news '
                              u'object, not specifically its content.'),
        source=u'collective.nitf.AvailableGenres',
    )

    section = schema.Choice(
        # nitf/head/pubdata/@position.section
        title=_(u'Section'),
        description=_(u'help_section',
                      default=u'Named section where the article will '
                              u'appear.'),
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
        missing_value=[],
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
                              u'place (as opposed to where the story was '
                              u'written).'),
        default=u'',
        missing_value=u'',
        required=False,
    )

    form.fieldset(
        'categorization',
        label=_(u'Categorization'),
        fields=['relatedItems', 'section', 'urgency', 'genre'],
    )


class NITF(Container):
    grok.implements(INITF)

    def is_empty(self):
        """Return True if the container has no files nor links inside.
        """
        content_filter = {'portal_type': ['File', 'Link']}
        return not self.listFolderContents(content_filter)

    # The purpose of these methods is to emulate those on News Item
    def getImage(self):
        """Return the first Image inside the News Article.
        """
        content_filter = {'portal_type': 'Image'}
        images = self.listFolderContents(content_filter)
        return images[0] if len(images) > 0 else None

    image = getImage  # XXX: a hack to support summary_view

    def imageCaption(self):
        image = self.getImage()
        if image is not None:
            return image.Description()

    def tag(self, **kwargs):
        # tag original implementation returns object title in both, alt and
        # title attributes
        image = self.getImage()
        if image is not None:
            scales = image.restrictedTraverse('@@images')
            if 'scale' in kwargs:
                scale_id = kwargs.get('scale')
                del kwargs['scale']
            else:
                scale_id = 'thumb'
            kwargs['alt'] = image.Description()
            kwargs['title'] = image.Title()
            scale = scales.scale(fieldname='image', scale=scale_id)
            return scale.tag(**kwargs)

    def image_thumb(self):
        """Return a thumbnail."""
        image = self.getImage()
        if image is not None:
            view = image.unrestrictedTraverse('@@images')
            # Return the data
            return view.scale(fieldname='image', scale='thumb').data


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
    text = obj.text
    if text:
        text = transformer(obj.text, 'text/plain')

    searchable_text = [safe_unicode(entry) for entry in (
        obj.id,
        obj.Title(),
        obj.subtitle,
        obj.Description(),
        obj.byline,
        text,
        obj.location,
    ) if entry]

    return u" ".join(searchable_text)

grok.global_adapter(textIndexer, name='SearchableText')
