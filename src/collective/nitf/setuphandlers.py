# -*- coding: utf-8 -*-

from zope import schema
from zope.component import getUtility
from zope.app.intid.interfaces import IIntIds

from Products.CMFCore.utils import getToolByName
from plone.registry import field
from plone.registry import Record
from plone.registry.interfaces import IRegistry

from collective.nitf import _
from collective.nitf import config

DEFAULT_KIND = 'collective.nitf.controlpanel.INITFSettings.default_kind'
EMBEDLY_KEY = 'collective.nitf.controlpanel.INITFSettings.embedly_key'

def updateControlPanelRegistry(portal):
    registry = getUtility(IRegistry, context=portal)


def updateIntIds(portal):
    catalog = getToolByName(portal, 'portal_catalog')
    intids = getUtility(IIntIds)

    results = catalog.searchResults()
    for res in results:
        nitf = res.getObject()
        if not intids.queryId(nitf):
            intids.register(nitf)

def setupVarious(context):
    # We check from our GenericSetup context whether we are running
    # add-on installation for your product or any other proudct
    if context.readDataFile('collective.nitf.marker.txt') is None:
        # Not your add-on
        return

    portal = context.getSite()
    updateControlPanelRegistry(portal)
    updateIntIds(portal)
