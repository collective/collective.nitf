# -*- coding:utf-8 -*-
from collective.nitf.config import PROJECTNAME
from plone import api

import logging
logger = logging.getLogger(PROJECTNAME)


def add_locking_behaviour(context):
    """Add locking behaviour to News Article."""
    locking_behavior = 'plone.app.lockingbehavior.behaviors.ILocking'
    types = api.portal.get_tool('portal_types')
    nitf = types['collective.nitf.content']
    behaviors = list(nitf.behaviors)
    behaviors.append(locking_behavior)
    nitf.behaviors = tuple(behaviors)
    logger.info('ILocking behavior added to News Article content type.')
