# -*- coding:utf-8 -*-

from collective.nitf.config import PROJECTNAME
from plone import api

import logging


def miscellaneous(context, logger=None):
    """Apply upgrade profile."""
    if logger is None:
        # Called as upgrade step: define our own logger
        logger = logging.getLogger(PROJECTNAME)

    # rename view on content type registry
    profile = 'profile-collective.nitf.upgrades.v20:to20alpha1'
    setup = api.portal.get_tool('portal_setup')
    setup.runAllImportStepsFromProfile(profile)


def update_layouts(context, logger=None):
    if logger is None:
        # Called as upgrade step: define our own logger
        logger = logging.getLogger(PROJECTNAME)

    # update existing objects
    logger.info(u'Updating News Articles layout')
    catalog = api.portal.get_tool('portal_catalog')
    results = catalog(portal_type='collective.nitf.content')
    i = 0
    for item in results:
        obj = item.getObject()
        if obj.getLayout() == 'nitf_galleria':
            obj.setLayout('galleria')
            i += 1
    logger.info(u'{0} News Articles updated'.format(i))
