# -*- coding: utf-8 -*-

import unittest2 as unittest

from AccessControl import Unauthorized

from zope.app.file.tests.test_image import zptlogo

from plone.app.testing import TEST_USER_ID
from plone.app.testing import logout
from plone.app.testing import setRoles

from collective.nitf import INITFBrowserLayer
from collective.nitf.testing import INTEGRATION_TESTING


class ViewTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        directlyProvides(self.request, INITFBrowserLayer)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']
        self.folder.invokeFactory('collective.nitf.content', 'n1')
        self.n1 = self.folder['n1']

    def test_view(self):
        view = self.n1.restrictedTraverse('newsitem_view')
        view.update()
        self.assertEquals(view.image(), None)
        self.n1.invokeFactory('Image', 'foo', image=StringIO(zptlogo))
        self.assertEquals(len(view.get_images()), 1)
        self.assertEquals(view.image()['id'], 'foo')

    def test_organize(self):
        # view can not be accessed by anonymous users
        logout()
        self.assertRaises(Unauthorized,
                          self.n1.restrictedTraverse,
                         '@@organize')

    def test_media_uploader(self):
        # view can not be accessed by anonymous users
        logout()
        self.assertRaises(Unauthorized,
                          self.n1.restrictedTraverse,
                         '@@media_uploader')


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)


from StringIO import StringIO

from zope.component import queryMultiAdapter
from zope.interface import directlyProvides

from collective.nitf.browser import MediaViewlet
from collective.nitf.browser import MediaLinksViewlet
from collective.nitf.testing import INTEGRATION_TESTING


class _TestNITFBrowser(unittest.TestCase):
    """ The tests begin with 4 NITF News Articles in the user's folder,
        self.folder. Each article has 2 Images, and the views should """

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.request = self.layer['request']
        directlyProvides(self.request, INITFBrowserLayer)
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']
        self.folder.invokeFactory('collective.nitf.content', 'n1')
        self.folder['n1'].title = u"Test NITF Article"
        self.add_image(self.folder['n1'], 'news-image-1')
        self.add_image(self.folder['n1'], 'news-image-2')
        self.folder['n1'].reindexObject()
        self.nitf = self.folder['n1']

    def add_image(self, container, m_id):
        container.invokeFactory('Image', id=m_id, title=u"Logo GIF",
                                image=StringIO(zptlogo))
        container[m_id].reindexObject()

    def test_media_view(self):
        view = queryMultiAdapter((self.nitf, self.request), name=u"media_view")
        self.assertNotEquals(view, None)
        view.update()
        image_count = len(view.get_images())
        self.assertEquals(image_count, 2)

    def _test_media_viewlet(self):
        view = queryMultiAdapter((self.nitf, self.request),
                                  name=u"newsitem_view")
        view.update()
        viewlet = MediaViewlet(self.nitf, self.request, view,
                                  'plone.abovecontentbody')
        self.assertNotEquals(viewlet, None)
        viewlet.update()

    def _test_links_viewlet(self):
        view = queryMultiAdapter((self.nitf, self.request),
                                  name=u"newsitem_view")
        view.update()
        viewlet = MediaLinksViewlet(self.nitf, self.request,
                                  view, 'plone.htmlhead.links')
        self.assertNotEquals(viewlet, None)
        viewlet.update()
        open('/tmp/viewlet.html', 'w').write(viewlet.render())
