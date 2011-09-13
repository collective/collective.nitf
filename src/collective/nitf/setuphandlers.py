# -*- coding: utf-8 -*-

from zope.component import getUtility
from zope.app.intid.interfaces import IIntIds

from Products.CMFCore.utils import getToolByName


# TODO: document why we're doing this
def updateIntIds(portal):
    catalog = getToolByName(portal, 'portal_catalog')
    intids = getUtility(IIntIds)

    results = catalog.searchResults()
    for brain in results:
        obj = brain.getObject()
        if not intids.queryId(obj):
            intids.register(obj)


def setupVarious(context):
    # We check from our GenericSetup context whether we are running add-on
    # installation for your product or any other product
    if context.readDataFile('collective.nitf.marker.txt') is None:
        # Not your add-on
        return

    portal = context.getSite()
    updateIntIds(portal)
