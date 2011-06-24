# -*- coding: utf-8 -*-

from five import grok
from zope import schema

from plone.directives import form, dexterity

from plone.app.textfield import RichText

from collective.nitf import _
from collective.nitf.config import PROPERTIES, URGENCIES, NORMAL


class INITF(form.Schema):
    """A news item based on the News Industry Text Format specification.
    """

    body = RichText(
            title=_(u'Body'),
            required=False,
        )

    property_ = schema.Choice(
            title=_(u'Property'),
            vocabulary=PROPERTIES,
        )

    section = schema.Text(
            title=_(u'Section'),
            required=False,
        )

    urgency = schema.Choice(
            title=_(u'Urgency'),
            vocabulary=URGENCIES,
            default=NORMAL,
        )

    byline = schema.Text(
            title=_(u'Author'),
            required=False,
        )


class NewsItem_View(grok.View):
    grok.context(INITF)
    grok.require('zope2.View')



