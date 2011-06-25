# -*- coding: utf-8 -*-

from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('collective.nitf')


class INITFBrowserLayer(IDefaultBrowserLayer):
    """Default browser layer for NITF content views."""

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
