# -*- coding: utf-8 -*-

from AccessControl import Unauthorized
from collective.nitf.interfaces import INITFLayer
from collective.nitf.testing import INTEGRATION_TESTING
from collective.nitf.controlpanel import INITFCharCountSettings
from plone.app.customerize import registration
from plone.app.testing import TEST_USER_ID, logout, setRoles
from plone.registry.interfaces import IRegistry
from StringIO import StringIO
from zope.app.file.tests.test_image import zptlogo
from zope.component import getMultiAdapter, queryMultiAdapter, getUtility

from zope.interface import directlyProvides

import unittest2 as unittest


class DefaultViewTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        directlyProvides(self.request, INITFLayer)

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

        self.folder.invokeFactory('collective.nitf.content', 'n1')
        self.n1 = self.folder['n1']

    def test_default_view_is_registered(self):
        pt = self.portal['portal_types']
        self.assertEqual(pt['collective.nitf.content'].default_view, 'view')

        registered = [v.name for v in registration.getViews(INITFLayer)]
        self.assertTrue('view' in registered)

    def test_chunks(self):
        """ Test is chunks are created from a list.
        """
        view = getMultiAdapter((self.n1, self.request), name='view')
        chunks = view._chunks
        # create chunks of 3 elements
        data = chunks([1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4], 3)
        # generator elements are accessed calling next()
        self.assertEqual(data.next(), [1, 1, 1])
        self.assertEqual(data.next(), [2, 2, 2])
        self.assertEqual(data.next(), [3, 3, 3])
        self.assertEqual(data.next(), [4, 4])

    def test_get_images_in_groups(self):
        view = getMultiAdapter((self.n1, self.request), name='view')
        groups = len([i for i in view.get_images_in_groups()])
        self.assertEqual(groups, 0)

        self.n1.invokeFactory('Image', 'foo', image=StringIO(zptlogo))
        groups = len([i for i in view.get_images_in_groups()])
        # we only have one image, so we only have one group
        self.assertEqual(groups, 1)


class ScrollableViewTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        directlyProvides(self.request, INITFLayer)

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

        self.folder.invokeFactory('collective.nitf.content', 'n1')
        self.n1 = self.folder['n1']

    def test_scrollable_view_is_registered(self):
        registered = [v.name for v in registration.getViews(INITFLayer)]
        self.assertTrue('scrollable' in registered)

        view = queryMultiAdapter((self.n1, self.request), name='scrollable')
        self.assertTrue(view is not None)


class NITFViewTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        directlyProvides(self.request, INITFLayer)

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

        self.folder.invokeFactory('collective.nitf.content', 'n1')
        self.n1 = self.folder['n1']

    def test_scrollable_view_is_registered(self):
        view = queryMultiAdapter((self.n1, self.request), name='nitf')
        self.assertTrue(view is not None)

    def test_get_mediatype(self):
        view = getMultiAdapter((self.n1, self.request), name='nitf')
        _get_mediatype = view._get_mediatype
        self.assertEqual(_get_mediatype('application/pdf'), 'application')
        self.assertEqual(_get_mediatype('audio/mpeg3'), 'audio')
        self.assertEqual(_get_mediatype('image/jpeg'), 'image')
        self.assertEqual(_get_mediatype('image/png'), 'image')
        self.assertEqual(_get_mediatype('multipart/signed'), 'other')
        self.assertEqual(_get_mediatype('text/plain'), 'text')
        self.assertEqual(_get_mediatype('video/avi'), 'video')

    def test_get_media(self):
        view = getMultiAdapter((self.n1, self.request), name='nitf')
        get_media = view.get_media
        self.assertEqual(len(get_media()), 0)

        self.n1.invokeFactory('Image', 'foo', image=StringIO(zptlogo))
        self.assertEqual(len(get_media()), 1)


class NewsMLViewTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        directlyProvides(self.request, INITFLayer)

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

        self.folder.invokeFactory('collective.nitf.content', 'n1')
        self.n1 = self.folder['n1']

    def test_newsml_view_is_registered(self):
        view = queryMultiAdapter((self.n1, self.request), name='newsml')
        self.assertTrue(view is not None)


class MediaViewTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        directlyProvides(self.request, INITFLayer)

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

        self.folder.invokeFactory('collective.nitf.content', 'n1')
        self.n1 = self.folder['n1']

    def test_media_view_is_registered(self):
        view = queryMultiAdapter((self.n1, self.request), name='media')
        self.assertTrue(view is not None)

    def test_media_view_is_protected(self):
        logout()
        self.assertRaises(Unauthorized, self.n1.restrictedTraverse, '@@media')


class CharacterCountJSTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

        self.folder.invokeFactory('collective.nitf.content', 'n1')
        self.n1 = self.folder['n1']

    def test_config_empty(self):
        view = getMultiAdapter((self.folder, self.request), name='characters-count.js')
        render = view.render()
        self.assertEqual(render, '$(document).ready(function() { });')

    def test_config_nitf(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(INITFCharCountSettings)
        settings.show_title_counter = True
        settings.show_description_counter = True
        view = getMultiAdapter((self.n1.restrictedTraverse('edit'), self.request), name='characters-count.js')
        render = view.render()
        self.assertEqual(render, '$(document).ready(function() {$("#form-widgets-IDublinCore-title").charCount({"optimal": 100, "counterText": "Characters left: ", "allowed": 100}); $("#form-widgets-IDublinCore-description").charCount({"optimal": 200, "counterText": "Characters left: ", "allowed": 200});});')
