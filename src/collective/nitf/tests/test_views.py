# -*- coding: utf-8 -*-
from collective.nitf.config import JS_RESOURCES
from collective.nitf.interfaces import INITFLayer
from collective.nitf.testing import FRACTAL
from collective.nitf.testing import INTEGRATION_TESTING
from collective.nitf.tests.api_hacks import set_file_field
from collective.nitf.tests.api_hacks import set_image_field
from plone import api
from plone.app.customerize import registration
from plone.app.testing import logout
from zope.interface import alsoProvides

import unittest


class TestViewMixin:

    def test_view_is_registered(self):
        registered = [v.name for v in registration.getViews(INITFLayer)]
        self.assertIn(self.name, registered)


class BaseViewTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        alsoProvides(self.request, INITFLayer)

        with api.env.adopt_roles(['Manager']):
            self.n1 = api.content.create(
                self.portal, 'collective.nitf.content', 'n1')


class DefaultViewTestCase(TestViewMixin, BaseViewTestCase):

    def setUp(self):
        super(DefaultViewTestCase, self).setUp()
        self.name = u'view'
        self.view = api.content.get_view(self.name, self.n1, self.request)

    def test_is_default_view(self):
        types = self.portal['portal_types']
        default_view = types['collective.nitf.content'].default_view
        self.assertEqual(default_view, u'view')

    # FIXME: we're getting: error while rendering collective.nitf.image
    def test_default_view_render(self):
        self.assertNotIn('<div id="media">', self.view())
        image = api.content.create(self.n1, 'Image', title='foo')
        set_image_field(image, FRACTAL, 'image/jpeg')
        self.assertIn('<div id="media">', self.view())

    def test_render_js_resources(self):
        rendered = self.view()
        for js in JS_RESOURCES:
            self.assertNotIn(js, rendered)

    def test_get_images(self):
        images = self.view.get_images()
        self.assertEqual(len(images), 0)

        image = api.content.create(self.n1, 'Image', title='foo', description='bar')
        set_image_field(image, FRACTAL, 'image/jpeg')
        images = self.view.get_images()
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0].getObject().Title(), 'foo')
        self.assertEqual(images[0].getObject().Description(), 'bar')

    def test_get_files(self):
        files = self.view.get_files()
        self.assertEqual(len(files), 0)

        file = api.content.create(self.n1, 'File', title='foo', description='bar')
        set_file_field(file, FRACTAL, 'image/jpeg')
        files = self.view.get_files()
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0].getObject().Title(), 'foo')
        self.assertEqual(files[0].getObject().Description(), 'bar')

    def test_get_links(self):
        links = self.view.get_links()
        self.assertEqual(len(links), 0)

        self.n1.invokeFactory('Link', 'foo', remoteUrl='http://foo/')
        links = self.view.get_links()
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0].getObject().id, 'foo')
        self.assertEqual(links[0].getObject().remoteUrl, 'http://foo/')

    def test_get_media(self):
        media = self.view.get_media()
        self.assertEqual(len(media), 0)

        image = api.content.create(self.n1, 'Image', title='foo')
        set_image_field(image, FRACTAL, 'image/jpeg')
        file = api.content.create(self.n1, 'File', title='bar')
        set_file_field(file, FRACTAL, 'image/jpeg')
        self.n1.invokeFactory('Link', 'baz', remoteUrl='http://baz/')
        media = self.view.get_media()
        self.assertEqual(len(media), 3)
        self.assertEqual(media[0].getObject().Title(), 'foo')
        self.assertEqual(media[1].getObject().id, 'bar')
        self.assertEqual(media[2].getObject().id, 'baz')


class SlideshowViewTestCase(TestViewMixin, BaseViewTestCase):

    def setUp(self):
        super(SlideshowViewTestCase, self).setUp()
        self.name = u'slideshow_view'
        self.view = api.content.get_view(self.name, self.n1, self.request)

    def test_slideshow_view_render(self):
        self.assertNotIn('<div class="slideshow-player">', self.view())
        self.assertNotIn('<div class="slideshow-pager">', self.view())
        image = api.content.create(self.n1, 'Image', 'foo')
        set_image_field(image, FRACTAL, 'image/jpeg')
        self.assertIn('<div class="slideshow-player">', self.view())
        self.assertIn('<div class="slideshow-pager">', self.view())

    def test_render_js_resources(self):
        rendered = self.view()
        for js in JS_RESOURCES:
            self.assertIn(js, rendered)


class TextOnlyViewTestCase(TestViewMixin, BaseViewTestCase):

    def setUp(self):
        super(TextOnlyViewTestCase, self).setUp()
        self.name = u'text_only_view'
        self.view = api.content.get_view(self.name, self.n1, self.request)

    def test_text_only_view_render(self):
        self.assertNotIn('<div id="media">', self.view())
        image = api.content.create(self.n1, 'Image', title='foo', description='bar')
        set_image_field(image, FRACTAL, 'image/jpeg')
        self.assertNotIn('<div id="media">', self.view())

    def test_render_js_resources(self):
        rendered = self.view()
        for js in JS_RESOURCES:
            self.assertNotIn(js, rendered)


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

        image = api.content.create(self.n1, 'Image', title='foo')
        set_image_field(image, FRACTAL, 'image/jpeg')
        self.assertEqual(len(get_media()), 1)


class NewsMLViewTestCase(BaseViewTestCase):

    def setUp(self):
        super(NewsMLViewTestCase, self).setUp()
        self.view = api.content.get_view(u'newsml', self.n1, self.request)

    def test_version(self):
        self.assertEqual(self.view.version(), 1)

    def test_nitf_size(self):
        self.assertEqual(self.view.nitf_size(), 1000)


class MediaViewTestCase(BaseViewTestCase):

    def test_media_view_is_protected(self):
        from AccessControl import Unauthorized
        logout()
        with self.assertRaises(Unauthorized):
            self.n1.restrictedTraverse('@@media')


class TraversalViewTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        with api.env.adopt_roles(['Manager']):
            self.n1 = api.content.create(
                self.portal, 'collective.nitf.content', 'n1')

    def test_images_traversal(self):
        from collective.nitf.testing import DEXTERITY_ONLY
        from collective.nitf.testing import IS_PLONE_5
        image = api.content.create(self.n1, 'Image', title='foo', description='bar')
        set_image_field(image, FRACTAL, 'image/jpeg')
        scale = self.n1.unrestrictedTraverse('@@images').scale('image')

        # FIXME: acquisition?
        if IS_PLONE_5 or DEXTERITY_ONLY:
            # (Pdb) scale
            # <plone.namedfile.scaling.ImageScale object at 0x7eff7b683650>
            self.assertEqual(scale.index_html(), FRACTAL)
        else:
            # (Pdb) scale
            # <plone.app.blob.field.BlobWrapper object at 0x7f85bdb6b8c0>
            self.assertEqual(scale.data, FRACTAL)
