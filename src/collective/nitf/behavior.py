# -*- coding: utf-8 *-*
""" Dexterity behavior to enable a local diazo theme.
"""
from zope.interface import alsoProvides, Interface
from zope import schema
from plone.directives import form
from collective.nitf import _


class IPin(Interface):
    """
    """
    pin = schema.Bool(title=_(u"Pin"),
                      description=_(u"Pin this nitf content."),
                      required=True,
                      default=False,
                      )

alsoProvides(IPin, form.IFormFieldProvider)
