# -*- coding: utf-8 -*-

from zope.interface import Interface
from plone.theme.interfaces import IDefaultPloneLayer


class INITFBrowserLayer(IDefaultPloneLayer):
    """A marker interface for the theme layer.
    """


class IMediaView(Interface):
    """Marker interface for media views.
    """
