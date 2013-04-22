# -*- coding: utf-8 -*-

from AccessControl import Unauthorized
from collective.nitf.controlpanel import INITFCharCountSettings
from collective.nitf.interfaces import INITFLayer
from collective.nitf.testing import INTEGRATION_TESTING
from collective.nitf.tests.test_content import zptlogo
from plone.app.customerize import registration
from plone.app.testing import TEST_USER_ID, logout, setRoles
from plone.registry.interfaces import IRegistry
from StringIO import StringIO
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
        self.assertIn('view', registered)

    def test_get_images(self):
        view = getMultiAdapter((self.n1, self.request), name='view')
        self.assertEqual(len(view.get_images()), 0)

        self.n1.invokeFactory('Image', 'foo', title='bar', description='baz',
                              image=StringIO(zptlogo))
        images = view.get_images()
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0].getObject().id, 'foo')
        self.assertEqual(images[0].getObject().Title(), 'bar')
        self.assertEqual(images[0].getObject().Description(), 'baz')

    def test_has_images(self):
        view = getMultiAdapter((self.n1, self.request), name='view')
        has_images = view.has_images
        self.assertEqual(has_images(), 0)

        self.n1.invokeFactory('Image', 'foo', image=StringIO(zptlogo))
        self.assertEqual(has_images(), 1)

    def test_get_files(self):
        view = getMultiAdapter((self.n1, self.request), name='view')
        self.assertEqual(len(view.get_files()), 0)

        self.n1.invokeFactory('File', 'foo', title='bar', description='baz',
                              image=StringIO(zptlogo))
        files = view.get_files()
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0].getObject().id, 'foo')
        self.assertEqual(files[0].getObject().Title(), 'bar')
        self.assertEqual(files[0].getObject().Description(), 'baz')

    def test_has_files(self):
        view = getMultiAdapter((self.n1, self.request), name='view')
        self.assertEqual(view.has_files(), 0)

        self.n1.invokeFactory('File', 'foo', image=StringIO(zptlogo))
        self.assertEqual(view.has_files(), 1)

    def test_get_links(self):
        view = getMultiAdapter((self.n1, self.request), name='view')
        self.assertEqual(len(view.get_links()), 0)

        self.n1.invokeFactory('Link', 'foo', remoteUrl='http://foo/')
        links = view.get_links()
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0].getObject().id, 'foo')
        self.assertEqual(links[0].getObject().remoteUrl, 'http://foo/')

    def test_has_links(self):
        view = getMultiAdapter((self.n1, self.request), name='view')
        self.assertEqual(view.has_links(), 0)

        self.n1.invokeFactory('Link', 'foo', remoteUrl='http://foo/')
        self.assertEqual(view.has_links(), 1)

    def test_get_media(self):
        view = getMultiAdapter((self.n1, self.request), name='view')
        self.assertEqual(len(view.get_media()), 0)

        self.n1.invokeFactory('Image', 'foo', image=StringIO(zptlogo))
        self.n1.invokeFactory('File', 'bar', file=StringIO(zptlogo))
        self.n1.invokeFactory('Link', 'baz', remoteUrl='http://baz/')
        media = view.get_media()
        self.assertEqual(len(media), 3)
        self.assertEqual(media[0].getObject().id, 'foo')
        self.assertEqual(media[1].getObject().id, 'bar')
        self.assertEqual(media[2].getObject().id, 'baz')


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
        self.assertIsNotNone(view)


class GalleriaViewTestCase(unittest.TestCase):
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

    def test_nitf_galleria_view_is_registered(self):
        registered = [v.name for v in registration.getViews(INITFLayer)]
        self.assertIn('nitf_galleria', registered)

        view = queryMultiAdapter((self.n1, self.request), name='nitf_galleria')
        self.assertIsNotNone(view)


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
        self.assertIsNotNone(view)

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
        self.assertEqual(
            render,
            '$(document).ready(function() {\
$("#form-widgets-IDublinCore-title").charCount({"optimal": 100, \
"counterText": "Characters left: ", "allowed": 100}); \
$("#form-widgets-IDublinCore-description").charCount({"optimal": 200, \
"counterText": "Characters left: ", "allowed": 200});});'
        )


class TraversalViewTestCase(unittest.TestCase):

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

    def test_images_traversal(self):
        self.n1.invokeFactory('Image', 'foo', title='bar', description='baz',
                              image=StringIO(zptlogo))
        view = getMultiAdapter((self.n1, self.request), name='images')

        image = view.scale('image')
        self.assertEqual(image.data, zptlogo)
