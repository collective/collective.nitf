# -*- coding: utf-8 -*-
from collective.nitf.logger import logger
from plone import api


RESOURCES_TO_FIX = {
    '++resource++collective.nitf/styles.css': '++resource++collective.nitf/nitf.css'
}


def _rename_resources(tool, from_to):
    for id in tool.getResourceIds():
        if id in from_to:
            tool.renameResource(id, from_to[id])


def fix_resources_references(setup_tool):
    """Fix resource references after static files reorganization."""

    css_tool = api.portal.get_tool('portal_css')
    _rename_resources(css_tool, RESOURCES_TO_FIX)
    logger.info('Updated css references.')
