# -*- coding:utf-8 -*-
from collective.nitf.logger import logger
from collective.nitf.upgrades.v2000 import get_valid_objects
from plone import api

import transaction


def reindex_searchable_text(setup_tool):
    """Reindex news articles to fix SearchableText."""
    logger.info('Reindexing the catalog')
    catalog = api.portal.get_tool('portal_catalog')
    results = catalog(portal_type='collective.nitf.content')
    logger.info(u'Found {0} news articles'.format(len(results)))
    for n, obj in enumerate(get_valid_objects(results), start=1):
        catalog.catalog_object(obj, idxs=['SearchableText'])
        if n % 1000 == 0:
            transaction.commit()
            logger.info('{0} items processed.'.format(n))

    transaction.commit()
    logger.info('Done.')
