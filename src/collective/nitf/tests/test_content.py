# -*- coding: utf-8 -*-

import unittest2 as unittest
from StringIO import StringIO

from zope.app.file.tests.test_image import zptlogo

from zope.component import createObject
from zope.component import queryUtility

from Products.CMFPlone.interfaces import INonStructuralFolder

from plone.app.referenceablebehavior.referenceable import IReferenceable

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

from plone.dexterity.interfaces import IDexterityFTI

from plone.uuid.interfaces import IAttributeUUID

from collective.nitf.content import INITF
from collective.nitf.testing import INTEGRATION_TESTING


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
        self.assertNotEqual(None, fti)

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
            from plone.app.lockingbehavior.behaviors import ILocking
            assert ILocking  # Pyflakes
        except ImportError:
            self.fail('ILocking behavior not available')

#    def test_is_non_structural_folder(self):
#        self.assertTrue(INonStructuralFolder.providedBy(self.n1))

    def test_is_not_non_structural_folder(self):
        """
        NITF CT doesn't implement INonStructuralFolder any longer
        to allow folder factories menu
        """
        self.assertFalse(INonStructuralFolder.providedBy(self.n1))

    def test_action_is_registered(self):
        fti = queryUtility(IDexterityFTI, name='collective.nitf.content')
        actions = [a.id for a in fti.listActions()]
        self.assertTrue('media' in actions)

    def test_getImage(self):
        self.assertEqual(self.n1.getImage(), None)

        self.n1.invokeFactory('Image', 'foo', title='bar', description='baz',
                              image=StringIO(zptlogo))
        image = self.n1.getImage()
        self.assertEqual(image.id, 'foo')
        self.assertEqual(image.Title(), 'bar')
        self.assertEqual(image.Description(), 'baz')

    def test_tag(self):
        tag = self.n1.tag
        self.assertEqual(tag(), None)
        self.n1.invokeFactory('Image', 'foo', title='bar', description='baz',
                              image=StringIO(zptlogo))
        # tag original implementation returns object title in both, alt and
        # title attributes
        expected = '<img src="http://nohost/plone/test-folder/n1/foo/' + \
                   'image" alt="bar" title="bar" height="16" width="16" />'
        self.assertEqual(tag(), expected)

        expected = '<img src="http://nohost/plone/test-folder/n1/foo/' + \
                   'image_preview" alt="bar" title="bar" height="16" ' + \
                   'width="16" />'
        self.assertEqual(tag(scale='preview'), expected)

        expected = '<img src="http://nohost/plone/test-folder/n1/foo/' + \
                   'image" alt="bar" title="bar" height="16" width="16" ' + \
                   'class="myClass" />'

        self.assertEqual(tag(css_class='myClass'), expected)

    def test_imageCaption(self):
        imageCaption = self.n1.imageCaption
        self.assertEqual(imageCaption(), None)
        self.n1.invokeFactory('Image', 'foo', title='bar', description='baz',
                              image=StringIO(zptlogo))
        self.assertEqual(imageCaption(), 'baz')
