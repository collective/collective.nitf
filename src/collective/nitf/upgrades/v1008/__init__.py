# -*- coding:utf-8 -*-
from collective.nitf.config import PROJECTNAME
from plone.app.upgrade.utils import loadMigrationProfile

import logging


def fix_collections(context):
    """Update to 1008 version."""
    logger = logging.getLogger(PROJECTNAME)
    collections = context.portal_catalog(portal_type='Collection')
    logger.info('About to update {0} objects'.format(len(collections)))
    for col in collections:
        obj = col.getObject()
        query = obj.getRawQuery()
        fixed_query = []
        for item in query:
            fixed_item = dict(item)
            if item['i'] == 'urgency':
                fixed_item['o'] = 'plone.app.querystring.operation.intselection.is'
            fixed_query.append(fixed_item)
        obj.setQuery(fixed_query)
        logger.info(
            'Collection %s at %s updated' % (col.id, col.getPath())
        )
    logger.info('Done')


def apply_profile(context):
    """Update to 1008 version."""
    logger = logging.getLogger(PROJECTNAME)
    profile = 'profile-collective.nitf.upgrades.v1008:default'
    loadMigrationProfile(context, profile)
    logger.info('Updated to version 1008')
