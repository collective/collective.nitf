# -*- coding: utf-8 -*-
from collective.nitf.logger import logger
from plone import api


OLD = '++resource++collective.nitf/styles.css'
NEW = '++resource++collective.nitf/nitf.css'


def fix_resources_references(setup_tool):
    """Fix resource references after static files reorganization."""
    css_tool = api.portal.get_tool('portal_css')
    if OLD in css_tool.getResourceIds():
        css_tool.getResource(OLD).setCompression('none')
        css_tool.renameResource(OLD, NEW)
    logger.info('Updated CSS references.')
