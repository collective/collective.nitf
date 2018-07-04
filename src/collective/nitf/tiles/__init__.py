# -*- coding: utf-8 -*-
from collective.nitf.logger import logger

import pkg_resources


package = pkg_resources.get_distribution('plone.app.tiles')
if package.version < '3.0.0':
    logger.error(
        'Tile support needs plone.app.tiles >= 3.0.0; '
        '"collective.nitf" tile may be unavailable')
