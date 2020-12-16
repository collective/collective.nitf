# -*- coding:utf-8 -*-
from collective.nitf.logger import logger
from collective.nitf.upgrades import get_valid_objects
from plone import api

import transaction


def reindex_searchable_text(setup_tool):
    """Reindex news articles to fix SearchableText."""
    test = 'test' in setup_tool.REQUEST  # used to ignore transactions on tests
    logger.info('Reindexing the catalog')
    catalog = api.portal.get_tool('portal_catalog')
    results = catalog(portal_type='collective.nitf.content')
    logger.info('Found {0} news articles'.format(len(results)))
    for n, obj in enumerate(get_valid_objects(results), start=1):
        catalog.catalog_object(obj, idxs=['SearchableText'])
        if n % 1000 == 0 and not test:
            transaction.commit()
            logger.info('{0} items processed.'.format(n))

    if not test:
        transaction.commit()
    logger.info('Done.')
