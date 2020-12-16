# -*- coding:utf-8 -*-
from collective.nitf.logger import logger
from collective.nitf.upgrades import get_valid_objects
from plone import api

import transaction


def remove_searchabletext_metadata(setup_tool):
    """Remove SearchableText metadata and reindex objects."""
    portal_catalog = api.portal.get_tool('portal_catalog')
    if 'SearchableText' in portal_catalog.schema():
        portal_catalog.delColumn('SearchableText')

    test = 'test' in setup_tool.REQUEST  # used to ignore transactions on tests
    results = portal_catalog()
    logger.info('Found {0} objects'.format(len(results)))
    n = 0
    catalog_object = portal_catalog.catalog_object
    for obj in get_valid_objects(results):
        catalog_object(obj, idxs=['id'])
        n += 1
        if n % 1000 == 0 and not test:
            transaction.commit()
            logger.info('{0} items processed.'.format(n))

    if not test:
        transaction.commit()
    logger.info('Done.')
