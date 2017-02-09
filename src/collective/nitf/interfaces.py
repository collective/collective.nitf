# -*- coding: utf-8 -*-
from collective.nitf import _
from collective.nitf.utils import genre_default_value
from collective.nitf.utils import urgency_default_value
from plone.app.textfield import RichText
from plone.autoform import directives as form
from plone.supermodel import model
from zope import schema
from zope.interface import Interface


class INITFLayer(Interface):
    """ A layer specific for this add-on product.
    """


class INITF(model.Schema):

    """A News Article based on the News Industry Text Format specification."""

    # title = schema.TextLine()
    # nitf/head/title and nitf/body/body.head/hedline/hl1

    form.order_before(subtitle='IDublinCore.title')
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

    model.fieldset('categorization', fields=['genre', 'urgency'])

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
        defaultFactory=genre_default_value
    )

    urgency = schema.Choice(
        # nitf/head/docdata/urgency/@ed-urg
        title=_(u'Urgency'),
        description=_(u'help_urgency',
                      default=u'News importance.'),
        vocabulary=u'collective.nitf.Urgencies',
        defaultFactory=urgency_default_value
    )
