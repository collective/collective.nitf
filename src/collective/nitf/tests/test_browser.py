# -*- coding: utf-8 -*-

import unittest2 as unittest

from AccessControl import Unauthorized
from StringIO import StringIO

from zope.app.file.tests.test_image import zptlogo
from zope.interface import directlyProvides

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
        view = self.n1.restrictedTraverse('view')
        view.update()
        self.assertEquals(view.image(), None)
        images = view.images()
        self.assertEquals(len(images), 0)
        files = view.files()
        self.assertEquals(len(files), 0)
        links = view.links()
        self.assertEquals(len(links), 0)
        self.n1.invokeFactory('Image', 'foo', image=StringIO(zptlogo))
        self.assertEquals(view.image()['id'], 'foo')
        images = view.images()
        self.assertEquals(len(images), 1)

    def test_gallery(self):
        self.n1.restrictedTraverse('newsmedia_view')

    def test_nitf(self):
        self.n1.restrictedTraverse('nitf')

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
