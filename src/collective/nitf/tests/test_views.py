# -*- coding: utf-8 -*-

import unittest2 as unittest

from StringIO import StringIO

from zope.app.file.tests.test_image import zptlogo
from zope.component import getMultiAdapter, queryMultiAdapter
from zope.interface import directlyProvides

from plone.app.customerize import registration

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from collective.nitf.interfaces import INITFBrowserLayer
from collective.nitf.testing import INTEGRATION_TESTING


class DefaultViewTestCase(unittest.TestCase):

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

    def test_default_view_is_registered(self):
        pt = self.portal['portal_types']
        self.assertEqual(pt['collective.nitf.content'].default_view, 'view')

        registered = [v.name for v in registration.getViews(INITFBrowserLayer)]
        self.assertTrue('view' in registered)

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

    def test_getImage(self):
        view = getMultiAdapter((self.n1, self.request), name='view')
        self.assertEqual(view.getImage(), None)

        self.n1.invokeFactory('Image', 'foo', title='bar', description='baz',
                              image=StringIO(zptlogo))
        image = view.getImage()
        self.assertEqual(image.id, 'foo')
        self.assertEqual(image.Title(), 'bar')
        self.assertEqual(image.Description(), 'baz')

    def test_tag(self):
        # TODO: test before adding image
        view = getMultiAdapter((self.n1, self.request), name='view')
        tag = view.tag
        self.n1.invokeFactory('Image', 'foo', title='bar', description='baz',
                              image=StringIO(zptlogo))
        # tag original implementation returns object title in both, alt and
        # title attributes
        self.assertEqual(tag(),
            '<img src="http://nohost/plone/test-folder/n1/foo/image" '
            'alt="bar" title="bar" height="16" width="16" />')
        self.assertEqual(tag(scale='preview'),
            '<img src="http://nohost/plone/test-folder/n1/foo/image_preview" '
            'alt="bar" title="bar" height="16" width="16" />')
        self.assertEqual(tag(css_class='myClass'),
            '<img src="http://nohost/plone/test-folder/n1/foo/image" '
            'alt="bar" title="bar" height="16" width="16" class="myClass" />')

    def test_imageCaption(self):
        # TODO: test before adding image
        view = getMultiAdapter((self.n1, self.request), name='view')
        self.n1.invokeFactory('Image', 'foo', title='bar', description='baz',
                              image=StringIO(zptlogo))
        self.assertEqual(view.imageCaption(), 'baz')

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
        directlyProvides(self.request, INITFBrowserLayer)

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

        self.folder.invokeFactory('collective.nitf.content', 'n1')
        self.n1 = self.folder['n1']

    def test_scrollable_view_is_registered(self):
        registered = [v.name for v in registration.getViews(INITFBrowserLayer)]
        self.assertTrue('scrollable' in registered)

        view = queryMultiAdapter((self.n1, self.request), name='scrollable')
        self.assertTrue(view is not None)


class NITFViewTestCase(unittest.TestCase):

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
        directlyProvides(self.request, INITFBrowserLayer)

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

        self.folder.invokeFactory('collective.nitf.content', 'n1')
        self.n1 = self.folder['n1']

    def test_newsml_view_is_registered(self):
        view = queryMultiAdapter((self.n1, self.request), name='newsml')
        self.assertTrue(view is not None)
