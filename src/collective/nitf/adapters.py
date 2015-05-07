# -*- coding: utf-8 -*-
from collective.nitf.content import INITF
from Products.CMFPlone.browser.syndication.adapters import DexterityItem
from Products.CMFPlone.interfaces.syndication import IFeed
from zope.component import adapts


class NitfItem(DexterityItem):
    adapts(INITF, IFeed)

    @property
    def author_name(self):
        return self.context.byline
