# -*- coding:utf-8 -*-
from collective.nitf.config import PROJECTNAME
from plone.app.upgrade.utils import loadMigrationProfile

import logging


def apply_profile(context):
    """Update to 1007 version."""
    logger = logging.getLogger(PROJECTNAME)
    profile = 'profile-collective.nitf.upgrades.v1007:default'
    loadMigrationProfile(context, profile)
    logger.info('Updated to version 1007')
