# -*- coding: utf-8 -*-

from zope.interface import Interface


class INITFLayer(Interface):
    """ A layer specific for this add-on product.
    """


class INewsMLFeed(Interface):
    """ A NewsML Feed
    """


class INewsMLSyndicatable(Interface):
    """ A NewsML object that can be syndicatable
    """
