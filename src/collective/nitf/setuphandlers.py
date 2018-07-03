# -*- coding: utf-8 -*-
from collective.nitf.config import PROJECTNAME
from plone import api
from Products.CMFPlone.interfaces import INonInstallable
from Products.CMFQuickInstallerTool import interfaces as BBB
from zope.interface import implementer

import logging


@implementer(BBB.INonInstallable)  # BBB: Plone 4.3
@implementer(INonInstallable)
class NonInstallable(object):  # pragma: no cover

    @staticmethod
    def getNonInstallableProducts():
        """Hide in the add-ons configlet."""
        return [
            u'collective.nitf.upgrades.v2003',
        ]

    @staticmethod
    def getNonInstallableProfiles(self):
        """Hide at site creation."""
        return [
            u'collective.nitf:uninstall',
            u'collective.nitf.upgrades.v2003:default',
        ]


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
    setup = api.portal.get_tool('portal_setup')
    setup.runImportStepFromProfile(profile, 'catalog')

    catalog = api.portal.get_tool('portal_catalog')
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
            logger.info('Added %s for field %s.', meta_type, name)

    if len(indexables) > 0:
        logger.info('Indexing new indexes %s.', ', '.join(indexables))
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
