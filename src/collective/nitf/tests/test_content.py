# -*- coding: utf-8 -*-

from collective.nitf.content import INITF
from collective.nitf.testing import INTEGRATION_TESTING
from plone.app.referenceablebehavior.referenceable import IReferenceable
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from plone.uuid.interfaces import IAttributeUUID
from Products.CMFPlone.interfaces import INonStructuralFolder
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

    def test_is_non_structural_folder(self):
        self.assertTrue(INonStructuralFolder.providedBy(self.n1))

    def test_action_is_registered(self):
        fti = queryUtility(IDexterityFTI, name='collective.nitf.content')
        actions = [a.id for a in fti.listActions()]
        self.assertTrue('media' in actions)
