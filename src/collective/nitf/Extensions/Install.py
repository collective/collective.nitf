# -*- coding: utf-8 -*-
from collective.nitf.config import PROJECTNAME
from plone import api


def remove_tile(portal):
    tiles = api.portal.get_registry_record('plone.app.tiles')
    if u'collective.nitf' in tiles:
        tiles.remove(u'collective.nitf')


def uninstall(portal, reinstall=False):
    if not reinstall:
        remove_tile(portal)
        profile = 'profile-%s:uninstall' % PROJECTNAME
        setup_tool = api.portal.get_tool('portal_setup')
        setup_tool.runAllImportStepsFromProfile(profile)
        return 'Ran all uninstall steps.'
