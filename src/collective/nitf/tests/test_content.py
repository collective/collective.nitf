# -*- coding: utf-8 -*-

from collective.nitf.content import INITF
from collective.nitf.testing import INTEGRATION_TESTING
from plone.app.referenceablebehavior.referenceable import IReferenceable
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from plone.uuid.interfaces import IAttributeUUID
from StringIO import StringIO
from zope.app.file.tests.test_image import zptlogo
from zope.component import createObject
from zope.component import queryUtility

import unittest2 as unittest


class ContentTypeTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

        self.folder.invokeFactory('collective.nitf.content', 'n1')
        self.n1 = self.folder['n1']

    def test_adding(self):
        self.assertTrue(INITF.providedBy(self.n1))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='collective.nitf.content')
        self.assertIsNotNone(fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='collective.nitf.content')
        schema = fti.lookupSchema()
        self.assertEqual(INITF, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='collective.nitf.content')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(INITF.providedBy(new_object))

    def test_is_referenceable(self):
        self.assertTrue(IReferenceable.providedBy(self.n1))
        self.assertTrue(IAttributeUUID.providedBy(self.n1))

    def test_locking_behavior_available(self):
        # ILocking is not applied by default, but must be available if needed
        try:
            from plone.app.lockingbehavior.behaviors import ILocking  # NOQA
        except ImportError:
            self.fail('ILocking behavior not available')

    def test_action_is_registered(self):
        fti = queryUtility(IDexterityFTI, name='collective.nitf.content')
        actions = [a.id for a in fti.listActions()]
        self.assertIn('media', actions)

    def test_getImage(self):
        self.assertIsNone(self.n1.getImage())

        self.n1.invokeFactory('Image', 'foo', title='bar', description='baz',
                              image=StringIO(zptlogo))
        image = self.n1.getImage()
        self.assertEqual(image.id, 'foo')
        self.assertEqual(image.Title(), 'bar')
        self.assertEqual(image.Description(), 'baz')

    def test_imageCaption(self):
        imageCaption = self.n1.imageCaption
        self.assertIsNone(imageCaption())
        self.n1.invokeFactory('Image', 'foo', title='bar', description='baz',
                              image=StringIO(zptlogo))
        self.assertEqual(imageCaption(), 'baz')

    def test_tag(self):
        tag = self.n1.tag

        # no images in news article, so no tag must be present
        self.assertIsNone(tag())

        self.n1.invokeFactory('Image', 'foo', title='bar', description='baz',
                              image=StringIO(zptlogo))

        # image title must be in both, alt and title attributes
        self.assertIn('alt="bar" title="bar"', tag())

        # image size
        self.assertIn('height="16" width="16', tag())

        # image scale
        self.assertIn('src="http://nohost/plone/test-folder/n1/foo/image_preview"',
                      tag(scale='preview'))

        # image class
        self.assertIn('class="myClass"', tag(css_class='myClass'))
