# -*- coding:utf-8 -*-

from collective.nitf.config import PROJECTNAME
from plone import api

import logging


def miscellaneous(context, logger=None):
    """Apply upgrade profile; this includes:

    - remove character counter resources from CSS and JS registries
    - remove character counter control panel records from registry
    - rename gallery view in News Article content type
    - cook CSS and JS resources
    """
    if logger is None:
        # Called as upgrade step: define our own logger
        logger = logging.getLogger(PROJECTNAME)

    profile = 'profile-collective.nitf.upgrades.v20:to20alpha1'
    setup = api.portal.get_tool('portal_setup')
    setup.runAllImportStepsFromProfile(profile)

    portal_css = api.portal.get_tool('portal_css')
    portal_css.cookResources()
    logger.info(u'CSS resources cooked')
    portal_js = api.portal.get_tool('portal_javascripts')
    portal_js.cookResources()
    logger.info(u'JS resources cooked')


def update_layouts(context, logger=None):
    if logger is None:
        # Called as upgrade step: define our own logger
        logger = logging.getLogger(PROJECTNAME)

    # update existing objects
    logger.info(u'Updating layout of News Articles')
    catalog = api.portal.get_tool('portal_catalog')
    results = catalog(portal_type='collective.nitf.content')
    logger.info(u'{0} News Articles found'.format(len(results)))
    i = 0
    for item in results:
        obj = item.getObject()
        if obj.getLayout() == 'nitf_galleria':
            obj.setLayout('galleria')
            i += 1
        logger.info(u'{0} News Articles updated'.format(i))
