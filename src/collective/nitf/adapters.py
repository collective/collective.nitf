# -*- coding: utf-8 -*-
from collective.nitf.content import INITF
from zope.component import adapts

try:
    from Products.CMFPlone.browser.syndication.adapters import DexterityItem
    from Products.CMFPlone.interfaces.syndication import IFeed
except ImportError:  # 4.2
    from collective.syndication.adapters import DexterityItem
    from collective.syndication.interfaces import IFeed


class NitfItem(DexterityItem):
    adapts(INITF, IFeed)

    @property
    def author_name(self):
        return self.context.byline
