# -*- coding:utf-8 -*-

from collective.nitf.config import PROJECTNAME
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import interfaces as Plone
from Products.CMFQuickInstallerTool import interfaces as QuickInstaller
from zope.interface import implements

import logging

PROFILE_ID = 'profile-collective.nitf:default'


class HiddenProfiles(object):
    implements(Plone.INonInstallable)

    def getNonInstallableProfiles(self):
        profiles = [
            'collective.nitf:uninstall',
            'collective.nitf.upgrades.v1007:default',
            'collective.nitf.upgrades.v1008:default',
        ]
        return profiles


class HiddenProducts(object):
    implements(QuickInstaller.INonInstallable)

    def getNonInstallableProducts(self):
        """Do not show on QuickInstaller's list of installable products."""
        profiles = [
            u'collective.nitf.upgrades.v1007',
            u'collective.nitf.upgrades.v1008',
        ]
        return profiles


class Empty:
    pass


def add_catalog_indexes(context, logger=None):
    """ Method to add our wanted indexes to the portal_catalog. See
    http://maurits.vanrees.org/weblog/archive/2009/12/catalog for more
    information.
    """
    def extras(title, index_type='Okapi BM25 Rank',
               lexicon_id='plone_lexicon'):
        # See http://old.zope.org/Members/dedalu/ZCTextIndex_python
        extras = Empty()
        extras.doc_attr = title
        extras.index_type = index_type
        extras.lexicon_id = lexicon_id
        return extras

    if logger is None:
        # Called as upgrade step: define our own logger
        logger = logging.getLogger(PROJECTNAME)

    profile = 'profile-collective.nitf:default'
    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(profile, 'catalog')

    catalog = getToolByName(context, 'portal_catalog')
    indexes = catalog.indexes()

    wanted = (
        ('subtitle', 'ZCTextIndex'),
        ('byline', 'ZCTextIndex'),
        ('genre', 'FieldIndex'),
        ('section', 'FieldIndex'),
        ('urgency', 'FieldIndex'),
        ('location', 'ZCTextIndex'),
        ('SearchableText', 'ZCTextIndex'),
    )

    indexables = []
    for name, meta_type in wanted:
        if name not in indexes:
            if meta_type == 'ZCTextIndex':
                catalog.addIndex(name, meta_type, extras(name))
            else:
                catalog.addIndex(name, meta_type)
            indexables.append(name)
            logger.info("Added %s for field %s.", meta_type, name)

    if len(indexables) > 0:
        logger.info("Indexing new indexes %s.", ', '.join(indexables))
        catalog.manage_reindexIndex(ids=indexables)


def import_various(context):
    """ Import step for configuration that is not handled in XML files.
    """
    # Only run step if a flag file is present
    if context.readDataFile('collective.nitf.marker.txt') is None:
        return

    logger = context.getLogger(PROJECTNAME)
    site = context.getSite()
    add_catalog_indexes(site, logger)


def add_galleria_js(context, logger=None):
    """
    """
    if logger is None:
        # Called as upgrade step: define our own logger
        logger = logging.getLogger(PROJECTNAME)

    profile = 'profile-collective.js.galleria:default'
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile(profile)


def remove_collapsible_js(context, logger=None):
    """
    """
    if logger is None:
        # Called as upgrade step: define our own logger
        logger = logging.getLogger(PROJECTNAME)

    portal_js = getToolByName(context, 'portal_javascripts')
    portal_css = getToolByName(context, 'portal_css')
    portal_js.manage_removeScript("++resource++collective.nitf/jquery.collapsible-v.2.1.3.js")
    portal_css.manage_removeStylesheet("++resource++collective.nitf/collapsible.css")


def charcount_control_panel_update(context):
    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'plone.app.registry')
    context.runImportStepFromProfile(PROFILE_ID, 'jsregistry')
    context.runImportStepFromProfile(PROFILE_ID, 'cssregistry')


def default_values_update(context, logger=None):
    """
    """
    if logger is None:
        # Called as upgrade step: define our own logger
        logger = logging.getLogger(PROJECTNAME)

    catalog = getToolByName(context, 'portal_catalog')
    for item in catalog(portal_type='collective.nitf.content'):
        obj = item.getObject()
        if None in (obj.id, obj.Title(), obj.subtitle,
                    obj.Description(), obj.byline, obj.text,
                    obj.location):
            obj.reindexObject(idxs=['SearchableText'])


def upgrade_z3cformwidgets(context, logger=None):
    """
    """
    if logger is None:
        # Called as upgrade step: define our own logger
        logger = logging.getLogger(PROJECTNAME)

    profile = 'profile-collective.z3cform.widgets:upgrade_1_to_2'
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile(profile)
