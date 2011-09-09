# -*- coding: utf-8 -*-

from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class INITFBrowserLayer(IDefaultBrowserLayer):
    """Default browser layer for NITF content views.
    """


class IMediaView(Interface):
    """Marker interface for media views.
    """
