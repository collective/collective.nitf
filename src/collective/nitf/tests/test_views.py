# -*- coding: utf-8 -*-

import unittest2 as unittest

from StringIO import StringIO

from zope.app.file.tests.test_image import zptlogo
from zope.interface import directlyProvides

from plone.app.customerize import registration

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from collective.nitf.interfaces import INITFBrowserLayer
from collective.nitf.testing import INTEGRATION_TESTING


class BrowserLayerTest(unittest.TestCase):

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

    def test_views_registered(self):
        views = ['view', 'scrollable', 'folder_summary_view']
        registered = [v.name for v in registration.getViews(INITFBrowserLayer)]
        # empty set only if all 'views' are 'registered'
        self.assertEquals(set(views) - set(registered), set([]))

    def test_default_view(self):
        pt = getattr(self.portal, 'portal_types')
        self.assertEquals(pt['collective.nitf.content'].default_view, 'view')

    def test_view(self):
        name = '@@view'
        try:
            self.n1.unrestrictedTraverse(name)
        except AttributeError:
            self.fail('%s has no view %s' % (self.n1, name))

        view = self.n1.restrictedTraverse(name)
        self.assertEquals(len(view.get_images()), 0)
        self.assertEquals(len(view.get_files()), 0)
        self.assertEquals(len(view.get_links()), 0)
        self.assertEquals(len(view.get_media()), 0)
        self.assertEquals(view.getImage(), None)

    def test_get_images(self):
        self.n1.invokeFactory('Image', 'foo', title='Foo', description='FOO',
                              image=StringIO(zptlogo), filename='zpt.gif')
        view = self.n1.restrictedTraverse('@@view')
        images = view.get_images()
        self.assertEquals(len(images), 1)
        self.assertEquals(images[0].getObject().id, 'foo')
        self.assertEquals(images[0].getObject().Title(), 'Foo')
        self.assertEquals(images[0].getObject().Description(), 'FOO')

    def test_get_files(self):
        self.n1.invokeFactory('File', 'bar', title='Bar', description='BAR',
                              image=StringIO(zptlogo), filename='zpt.gif')
        view = self.n1.restrictedTraverse('@@view')
        files = view.get_files()
        self.assertEquals(len(files), 1)
        self.assertEquals(files[0].getObject().id, 'bar')
        self.assertEquals(files[0].getObject().Title(), 'Bar')
        self.assertEquals(files[0].getObject().Description(), 'BAR')

    def test_get_links(self):
        self.n1.invokeFactory('Link', 'baz', title='Baz', url='http://baz/')
        view = self.n1.restrictedTraverse('@@view')
        links = view.get_links()
        self.assertEquals(len(links), 1)
        self.assertEquals(links[0].getObject().id, 'baz')
        self.assertEquals(links[0].getObject().title, 'Baz')
        self.assertEquals(links[0].getObject().description, '')

    def test_get_media(self):
        self.n1.invokeFactory('Image', 'foo', title='Foo', image=StringIO(zptlogo))
        self.n1.invokeFactory('File', 'bar', title='Bar', file=StringIO(zptlogo))
        self.n1.invokeFactory('Link', 'baz', title='Baz', url='http://baz/')
        view = self.n1.restrictedTraverse('@@view')
        media = view.get_media()
        self.assertEquals(len(media), 3)
        self.assertEquals(media[0].getObject().id, 'foo')
        self.assertEquals(media[1].getObject().id, 'bar')
        self.assertEquals(media[2].getObject().id, 'baz')

    def test_getImage(self):
        self.n1.invokeFactory('Image', 'foo', title='Foo', description='FOO',
                              image=StringIO(zptlogo), filename='zpt.gif')
        view = self.n1.restrictedTraverse('@@view')
        image = view.getImage()
        self.assertEquals(image.id, 'foo')
        self.assertEquals(image.Title(), 'Foo')
        self.assertEquals(image.Description(), 'FOO')

    def test_tag(self):
        self.n1.invokeFactory('Image', 'foo', title='Foo', description='FOO',
                              image=StringIO(zptlogo), filename='zpt.gif')
        view = self.n1.restrictedTraverse('@@view')
        tag = view.tag
        self.assertEquals(tag(),
            '<img src="http://nohost/plone/test-folder/n1/foo/image" '
            'alt="Foo" title="Foo" height="16" width="16" />')
        self.assertEquals(tag(scale='preview'),
            '<img src="http://nohost/plone/test-folder/n1/foo/image_preview" '
            'alt="Foo" title="Foo" height="16" width="16" />')
        self.assertEquals(tag(css_class='myClass'),
            '<img src="http://nohost/plone/test-folder/n1/foo/image" '
            'alt="Foo" title="Foo" height="16" width="16" class="myClass" />')

    def test_imageCaption(self):
        self.n1.invokeFactory('Image', 'foo', title='Foo', description='FOO',
                              image=StringIO(zptlogo), filename='zpt.gif')
        view = self.n1.restrictedTraverse('@@view')
        self.assertEquals(view.imageCaption(), 'FOO')

    def test_chunks(self):
        """ Test is chunks are created from a list.
        """
        view = self.n1.restrictedTraverse('@@view')
        chunks = view._chunks
        # create chunks of 3 elements
        data = chunks([1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4], 3)
        # generator elements are accessed calling next()
        self.assertEquals(data.next(), [1, 1, 1])
        self.assertEquals(data.next(), [2, 2, 2])
        self.assertEquals(data.next(), [3, 3, 3])
        self.assertEquals(data.next(), [4, 4])

    def test_get_images_in_groups(self):
        self.n1.invokeFactory('Image', 'foo', title='Foo', description='FOO',
                              image=StringIO(zptlogo), filename='zpt.gif')
        view = self.n1.restrictedTraverse('@@view')
        groups = len([i for i in view.get_images_in_groups()])
        # we only have one image, so we only have one group
        self.assertEquals(groups, 1)

    def test_scrollable(self):
        name = '@@scrollable'
        try:
            self.n1.unrestrictedTraverse(name)
        except AttributeError:
            self.fail('%s has no view %s' % (self.n1, name))

    def test_folder_summary_view(self):
        name = '@@folder_summary_view'
        try:
            self.n1.unrestrictedTraverse(name)
        except AttributeError:
            self.fail('%s has no view %s' % (self.n1, name))

    def test_viewlets_registered(self):
        NotImplemented


class NITFViewTest(unittest.TestCase):

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

    def test_nitf(self):
        # this view is available but not registered
        name = '@@nitf'
        try:
            self.n1.unrestrictedTraverse(name)
        except AttributeError:
            self.fail('%s has no view %s' % (self.n1, name))

    def test_get_mediatype(self):
        view = self.n1.restrictedTraverse('@@nitf')
        _get_mediatype = view._get_mediatype
        self.assertEquals(_get_mediatype('application/pdf'), 'application')
        self.assertEquals(_get_mediatype('audio/mpeg3'), 'audio')
        self.assertEquals(_get_mediatype('image/jpeg'), 'image')
        self.assertEquals(_get_mediatype('image/png'), 'image')
        self.assertEquals(_get_mediatype('multipart/signed'), 'other')
        self.assertEquals(_get_mediatype('text/plain'), 'text')
        self.assertEquals(_get_mediatype('video/avi'), 'video')

    def test_get_media(self):
        self.n1.invokeFactory('Image', 'foo', title='Foo', description='FOO',
                              image=StringIO(zptlogo), filename='zpt.gif')
        view = self.n1.restrictedTraverse('@@nitf')
        media = view.get_media()
        self.assertEquals(len(media), 1)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
