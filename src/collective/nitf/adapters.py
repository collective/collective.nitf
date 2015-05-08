# -*- coding: utf-8 -*-
from collective.nitf.config import PLONE_VERSION
from collective.nitf.content import INITF
from zope.component import adapts

if PLONE_VERSION >= '4.3':
    from Products.CMFPlone.browser.syndication.adapters import DexterityItem
    from Products.CMFPlone.interfaces.syndication import IFeed
else:  # 4.2
    from collective.syndication.adapters import DexterityItem
    from collective.syndication.interfaces import IFeed


class NitfItem(DexterityItem):
    adapts(INITF, IFeed)

    @property
    def author_name(self):
        return self.context.byline
