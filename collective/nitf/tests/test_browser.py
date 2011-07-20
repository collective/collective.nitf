# -*- coding: utf-8 -*-

"""
$Id$
"""

import unittest2 as unittest

from zope.component import createObject
from zope.component import getMultiAdapter
from zope.component import queryMultiAdapter
from zope.component import queryUtility
from zope.publisher.browser import TestRequest

from Products.CMFPlone.utils import getToolByName
from plone.dexterity.interfaces import IDexterityFTI

from collective.transmogrifier.transmogrifier import Transmogrifier
from collective.nitf.content import INITF
from collective.nitf.content import MediaViewlet
from collective.nitf.content import MediaLinksViewlet
from collective.nitf.testing import INTEGRATION_TESTING


class TestNITFBrowser(unittest.TestCase):
    """ The tests begin with 4 NITF News Articles in the user's folder,
        self.folder. Each article has 2 Images, and the views should """

    layer = INTEGRATION_TESTING

    def test_media_view(self):
        view = getMultiAdapter((self.folder.n1, TestRequest()), name="media_view")
        self.assertNotEquals(view, None)
        view.update()
        image_count = len(view.get_images())
        self.assertEquals(image_count, 2)

    def _test_newsitem_view(self):
        view = queryMultiAdapter((self.folder.n1, TestRequest()),
                                  name=u"newsitem_view")
        self.assertNotEquals(view, None)
        view.update()
        image_count = len(view.get_images())
        self.assertEquals(image_count, 2)

    def _test_media_viewlet(self):
        view = queryMultiAdapter((self.folder.n1, TestRequest()),
                                  name=u"newsitem_view")
        view.update()
        viewlet = MediaViewlet(self.folder.n1, TestRequest(), view,
                                  'plone.abovecontentbody')
        self.assertNotEquals(viewlet, None)
        viewlet.update()

    def _test_media_viewlet(self):
        view = queryMultiAdapter((self.folder.n1, TestRequest()),
                                  name=u"newsitem_view")
        view.update()
        viewlet = MediaViewlet(self.folder.n1, TestRequest(), view,
                                  'plone.abovecontentbody')
        self.assertNotEquals(viewlet, None)
        viewlet.update()

    def _test_links_viewlet(self):
        view = queryMultiAdapter((self.folder.n1, TestRequest()),
                                  name=u"newsitem_view")
        view.update()
        viewlet = MediaLinksViewlet(self.folder.n1, TestRequest(),
                                  view, 'plone.htmlhead.links')
        self.assertNotEquals(viewlet, None)
        viewlet.update()
        open('/tmp/viewlet.html', 'w').write(viewlet.render())


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
