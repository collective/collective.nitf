# -*- coding: utf-8 -*-

from collective.nitf import _
from collective.nitf.controlpanel import INITFSettings
from plone.app.dexterity import PloneMessageFactory as _PMF
from plone.app.textfield import RichText
from plone.app.textfield.interfaces import ITransformer
from plone.dexterity.content import Container
from plone.directives import form
from plone.indexer import indexer
from plone.registry.interfaces import IRegistry
from Products.CMFPlone.utils import safe_unicode
from zope import schema
from zope.component import getUtility
from zope.interface import implements


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
        default=u'',
        missing_value=u'',
        required=False,
    )

    byline = schema.TextLine(
        # nitf/body/body.head/byline/person
        title=_(u'Author'),
        default=u'',
        missing_value=u'',
        required=False,
    )

    location = schema.TextLine(
        # nitf/body/body.head/dateline/location
        title=_(u'Location'),
        description=_(
            u'help_location',
            default=u'Event location. Where an event took place '
                    u'(as opposed to where the story was written).',
        ),
        default=u'',
        missing_value=u'',
        required=False,
    )

    text = RichText(
        # nitf/body/body.content
        title=_(u'Body text'),
        required=False,
    )

    form.fieldset(
        'categorization',
        label=_PMF(u'label_schema_categorization', default=u'Categorization'),
        fields=['section', 'genre', 'urgency'],
    )

    form.order_before(section='subjects')
    section = schema.Choice(
        # nitf/head/pubdata/@position.section
        title=_(u'Section'),
        description=_(
            u'help_section',
            default=u'Named section where the article will appear.',
        ),
        vocabulary=u'collective.nitf.AvailableSections',
    )

    genre = schema.Choice(
        # nitf/head/tobject/tobject.property/@tobject.property.type
        title=_(u'Genre'),
        description=_(
            u'help_genre',
            default=u'Describes the nature, journalistic or '
                    u'intellectual characteristic of a news '
                    u'object, not specifically its content.',
        ),
        vocabulary=u'collective.nitf.AvailableGenres',
    )

    urgency = schema.Choice(
        # nitf/head/docdata/urgency/@ed-urg
        title=_(u'Urgency'),
        description=_(u'help_urgency',
                      default=u'News importance.'),
        vocabulary=u'collective.nitf.Urgencies',
    )


class NITF(Container):
    implements(INITF)

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
