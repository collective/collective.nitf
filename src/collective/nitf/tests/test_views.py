# -*- coding: utf-8 -*-

from AccessControl import Unauthorized
from collective.nitf.controlpanel import INITFCharCountSettings
from collective.nitf.interfaces import INITFLayer
from collective.nitf.testing import INTEGRATION_TESTING
from collective.nitf.tests.test_content import zptlogo
from plone import api
from plone.app.customerize import registration
from plone.app.testing import logout
from plone.registry.interfaces import IRegistry
from StringIO import StringIO
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.interface import directlyProvides

import unittest


class BaseViewTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        directlyProvides(self.request, INITFLayer)

        with api.env.adopt_roles(['Manager']):
            self.folder = api.content.create(self.portal, 'Folder', 'folder')

        self.folder.invokeFactory('collective.nitf.content', 'n1')
        self.n1 = self.folder['n1']


class DefaultViewTestCase(BaseViewTestCase):

    def setUp(self):
        super(DefaultViewTestCase, self).setUp()
        self.view = api.content.get_view(u'view', self.n1, self.request)

    def test_default_view_is_registered(self):
        pt = self.portal['portal_types']
        self.assertEqual(pt['collective.nitf.content'].default_view, u'view')

        registered = [v.name for v in registration.getViews(INITFLayer)]
        self.assertIn(u'view', registered)

    def test_get_images(self):
        images = self.view.get_images()
        self.assertEqual(len(images), 0)

        self.n1.invokeFactory(
            'Image', 'foo', title='bar', description='baz', image=StringIO(zptlogo))
        images = self.view.get_images()
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0].getObject().id, 'foo')
        self.assertEqual(images[0].getObject().Title(), 'bar')
        self.assertEqual(images[0].getObject().Description(), 'baz')

    def test_has_images(self):
        has_images = self.view.has_images
        self.assertEqual(has_images(), 0)

        self.n1.invokeFactory('Image', 'foo', image=StringIO(zptlogo))
        self.assertEqual(has_images(), 1)

    def test_get_files(self):
        files = self.view.get_files()
        self.assertEqual(len(files), 0)

        self.n1.invokeFactory(
            'File', 'foo', title='bar', description='baz', file=StringIO(zptlogo))
        files = self.view.get_files()
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0].getObject().id, 'foo')
        self.assertEqual(files[0].getObject().Title(), 'bar')
        self.assertEqual(files[0].getObject().Description(), 'baz')

    def test_has_files(self):
        self.assertEqual(self.view.has_files(), 0)

        self.n1.invokeFactory('File', 'foo', file=StringIO(zptlogo))
        self.assertEqual(self.view.has_files(), 1)

    def test_get_links(self):
        links = self.view.get_links()
        self.assertEqual(len(links), 0)

        self.n1.invokeFactory('Link', 'foo', remoteUrl='http://foo/')
        links = self.view.get_links()
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0].getObject().id, 'foo')
        self.assertEqual(links[0].getObject().remoteUrl, 'http://foo/')

    def test_has_links(self):
        self.assertEqual(self.view.has_links(), 0)

        self.n1.invokeFactory('Link', 'foo', remoteUrl='http://foo/')
        self.assertEqual(self.view.has_links(), 1)

    def test_get_media(self):
        media = self.view.get_media()
        self.assertEqual(len(media), 0)

        self.n1.invokeFactory('Image', 'foo', image=StringIO(zptlogo))
        self.n1.invokeFactory('File', 'bar', file=StringIO(zptlogo))
        self.n1.invokeFactory('Link', 'baz', remoteUrl='http://baz/')
        media = self.view.get_media()
        self.assertEqual(len(media), 3)
        self.assertEqual(media[0].getObject().id, 'foo')
        self.assertEqual(media[1].getObject().id, 'bar')
        self.assertEqual(media[2].getObject().id, 'baz')


class NITFViewTestCase(BaseViewTestCase):

    def setUp(self):
        super(NITFViewTestCase, self).setUp()
        self.view = api.content.get_view(u'nitf', self.n1, self.request)

    def test_get_mediatype(self):
        _get_mediatype = self.view._get_mediatype
        self.assertEqual(_get_mediatype('application/pdf'), 'application')
        self.assertEqual(_get_mediatype('audio/mpeg3'), 'audio')
        self.assertEqual(_get_mediatype('image/jpeg'), 'image')
        self.assertEqual(_get_mediatype('image/png'), 'image')
        self.assertEqual(_get_mediatype('multipart/signed'), 'other')
        self.assertEqual(_get_mediatype('text/plain'), 'text')
        self.assertEqual(_get_mediatype('video/avi'), 'video')

    def test_get_media(self):
        get_media = self.view.get_media
        self.assertEqual(len(get_media()), 0)

        self.n1.invokeFactory('Image', 'foo', image=StringIO(zptlogo))
        self.assertEqual(len(get_media()), 1)


class NewsMLViewTestCase(BaseViewTestCase):

    def setUp(self):
        super(NewsMLViewTestCase, self).setUp()
        self.view = api.content.get_view(u'newsml', self.n1, self.request)

    def test_version(self):
        self.assertEqual(self.view.version(), 1)

    def test_nitf_size(self):
        self.assertEqual(self.view.nitf_size(), 1000)


class GalleriaViewTestCase(BaseViewTestCase):

    def test_galleria_view_is_registered(self):
        registered = [v.name for v in registration.getViews(INITFLayer)]
        self.assertIn('galleria', registered)

        # raises InvalidParameterError if the view is not registered
        api.content.get_view(u'galleria', self.n1, self.request)


class MediaViewTestCase(BaseViewTestCase):

    def test_media_view_is_protected(self):
        logout()
        with self.assertRaises(Unauthorized):
            self.n1.restrictedTraverse('@@media')


class CharacterCountJSTestCase(BaseViewTestCase):

    def test_config_empty(self):
        view = api.content.get_view(u'characters-count.js', self.n1, self.request)
        self.assertEqual(view(), '$(document).ready(function() { });')

    def test_config_nitf(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(INITFCharCountSettings)
        settings.show_title_counter = True
        settings.show_description_counter = True
        view = getMultiAdapter((self.n1.restrictedTraverse('edit'), self.request), name='characters-count.js')
        self.assertEqual(
            view(),
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

        with api.env.adopt_roles(['Manager']):
            self.folder = api.content.create(self.portal, 'Folder', 'folder')

        self.folder.invokeFactory('collective.nitf.content', 'n1')
        self.n1 = self.folder['n1']

    def test_images_traversal(self):
        self.n1.invokeFactory(
            'Image', 'foo', title='bar', description='baz', image=StringIO(zptlogo))

        scales = self.n1.unrestrictedTraverse('@@images')
        image = scales.scale('image')
        self.assertEqual(image.data, zptlogo)


class RegisteredViewsTestCase(BaseViewTestCase):

    def test_registered_views(self):
        registered = [v.name for v in registration.getViews(INITFLayer)]
        for view in ('edit', 'nitf', u'l10n.datepicker', 'characters-count.js',
                     'newsml', 'media', 'galleria', 'view'):
            self.assertTrue(view in registered)
