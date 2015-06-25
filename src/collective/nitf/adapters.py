# -*- coding: utf-8 -*-
from collective.nitf.interfaces import INITF
from Products.CMFPlone.browser.syndication.adapters import DexterityItem
from Products.CMFPlone.interfaces.syndication import IFeed
from zope.component import adapts


class BylineFeed(DexterityItem):

    """Adapter to honor the author of a News Article in the syndication feed."""

    adapts(INITF, IFeed)

    @property
    def author_name(self):
        return self.context.byline
