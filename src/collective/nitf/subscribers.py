# -*- coding: utf-8 -*-

from five import grok
from zope.component import queryUtility
from zope.app.container.interfaces import IObjectAddedEvent
from zope.app.intid.interfaces import IIntIds

from Products.CMFCore.interfaces import IContentish
from Products.CMFCore.utils import getToolByName

@grok.subscribe(IContentish, IObjectAddedEvent)
def makeIntId(context, event):
    portal_url = getToolByName(context, "portal_url")
    portal = portal_url.getPortalObject()
    intids = queryUtility(IIntIds)
    if intids:
        if not intids.queryId(context):
            intids.register(context)
