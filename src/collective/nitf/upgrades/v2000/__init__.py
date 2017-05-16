# -*- coding:utf-8 -*-
from collective.nitf.config import PROJECTNAME
from collective.nitf.logger import logger
from plone import api
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import getUtility

import transaction


def get_valid_objects(brains):
    """Generate a list of objects associated with valid brains."""
    for b in brains:
        try:
            obj = b.getObject()
        except KeyError:
            obj = None

        if obj is None:  # warn on broken entries in the catalog
            logger.warn(
                u'Invalid reference in the catalog: {0}'.format(b.getPath()))
            continue
        yield obj


def apply_profile(setup_tool):
    """Apply upgrade profile; this includes:

    - remove character counter resources from CSS and JS registries
    - remove character counter control panel records from registry
    - rename galleria view in News Article content type
    """
    profile = 'profile-collective.nitf.upgrades.v2000:default'
    setup_tool.runAllImportStepsFromProfile(profile)


def update_layouts(setup_tool):
    # update existing objects
    logger.info(u'Updating layout of news articles')
    results = api.content.find(portal_type='collective.nitf.content')
    logger.info(u'Found {0} news articles'.format(len(results)))
    i = 0
    for obj in get_valid_objects(results):
        if obj.getLayout() == 'nitf_galleria':
            obj.setLayout('slideshow_view')
            i += 1
        logger.info(u'{0} news articles updated'.format(i))


def install_new_dependencies(setup_tool):
    dependencies = ('collective.js.cycle2',)
    qi = api.portal.get_tool('portal_quickinstaller')
    for p in dependencies:
        if not qi.isProductInstalled(p):
            qi.installProducts([p])
            logger.info(u'{0} installed'.format(p))


def update_configlet(setup_tool):
    """Update control panel configlet."""
    profile = 'profile-{0}:default'.format(PROJECTNAME)
    setup_tool.runImportStepFromProfile(profile, 'controlpanel')
    logger.info('Control panel configlet updated.')


BEHAVIORS_TO_ADD = frozenset([
    'plone.app.relationfield.behavior.IRelatedItems',
    'collective.nitf.behaviors.interfaces.ISection',
])


def update_behaviors(setup_tool):
    """Update News Article behaviors."""
    fti = getUtility(IDexterityFTI, name='collective.nitf.content')
    fti.behaviors = tuple(set(fti.behaviors) | BEHAVIORS_TO_ADD)
    logger.info('News Article behaviors updated.')


def reindex_news_articles(setup_tool):
    """Reindex news articles to fix interfaces."""
    test = 'test' in setup_tool.REQUEST  # used to ignore transactions on tests
    logger.info(
        u'Reindexing the catalog. '
        u'This process could take a long time on large sites. Be patient.'
    )
    catalog = api.portal.get_tool('portal_catalog')
    results = api.content.find(portal_type='collective.nitf.content')
    logger.info(u'Found {0} news articles'.format(len(results)))
    n = 0
    for obj in get_valid_objects(results):
        catalog.catalog_object(obj, idxs=['object_provides'], update_metadata=False)
        n += 1
        if n % 1000 == 0 and not test:
            transaction.commit()
            logger.info('{0} items processed.'.format(n))

    if not test:
        transaction.commit()
    logger.info('Done.')
