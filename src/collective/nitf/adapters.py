# -*- coding: utf-8 -*-
from collective.nitf.content import INITF
from zope.component import adapts

try:
    # Plone >= 4.3
    from Products.CMFPlone.browser.syndication.adapters import DexterityItem
    from Products.CMFPlone.interfaces.syndication import IFeed
except ImportError:
    # Plone 4.2
    from collective.syndication.adapters import DexterityItem
    from collective.syndication.interfaces import IFeed


class BylineFeed(DexterityItem):

    """Adapter to honor the author of a News Article in the syndication feed."""

    adapts(INITF, IFeed)

    @property
    def author_name(self):
        return self.context.byline
