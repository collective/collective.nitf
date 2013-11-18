# -*- coding: utf-8 -*-

from collective.nitf.setuphandlers import upgrade_to_1008
from collective.nitf.setuphandlers import upgrade_to_1009
from collective.nitf.setuphandlers import update_galleria_layout
from collective.nitf.setuphandlers import upgrade_to_1010
from collective.nitf.testing import INTEGRATION_TESTING
from plone.app.relationfield.behavior import IRelatedItems
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import queryUtility
from zope.intid.interfaces import IIntIds

import unittest


class Upgradeto1008TestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_update_dependencies(self):
        """Test plone.app.relationfield was installed.
        """
        qi = self.portal.portal_quickinstaller
        dependency = 'plone.app.relationfield'

        # manually uninstall resources to simulate previous profile
        if qi.isProductInstalled(dependency):
            qi.uninstallProducts([dependency])
        self.assertFalse(qi.isProductInstalled(dependency))

        # run the upgrade step and test resources are installed
        upgrade_to_1008(self.portal)
        self.assertTrue(qi.isProductInstalled(dependency))
        # TODO: move this out of the upgrade step test
        self.assertIsNotNone(queryUtility(IIntIds))


class Upgradeto1009TestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_irelated_behavior(self):
        """ Test the IRelatedItems behavior is installed by default.
            Then removed, to simulate previous profile
            And is added back once upgraded
        """

        # IRelatedItems is installed by default
        ttool = self.portal['portal_types']
        fti = ttool['collective.nitf.content']
        self.assertIn(
            'plone.app.relationfield.behavior.IRelatedItems', fti.behaviors)

        # Remove behavior to simulate previous profile
        behaviors = list(fti.behaviors)
        behaviors.remove('plone.app.relationfield.behavior.IRelatedItems')
        fti.behaviors = behaviors

        # NITF doesn't provide IRelatedItems (as expected)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('collective.nitf.content', 'n1')
        n1 = self.portal['n1']
        self.assertFalse(IRelatedItems.providedBy(n1))

        # run the upgrade step and verify everything works as expected
        upgrade_to_1009(self.portal)
        self.assertTrue(IRelatedItems.providedBy(n1))
        self.assertIn(
            'plone.app.relationfield.behavior.IRelatedItems', fti.behaviors)


class Upgradeto1010TestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_jsregistry(self):
        """ Test the new JS is correctly added to the registry by default
            Then removed, to simulate previous profile
            And is added back once upgraded
        """

        jstool = self.portal['portal_javascripts']
        new_js = '++resource++collective.nitf/nitf.js'
        self.assertIn(new_js, jstool.getResourceIds())
        jstool.unregisterResource(new_js)
        self.assertNotIn(new_js, jstool.getResourceIds())

        upgrade_to_1010(self.portal)

        self.assertIn(new_js, jstool.getResourceIds())

    def test_update_layout(self):
        """ Test old nitf_galleria layout is properly changed for galleria
        """

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('collective.nitf.content', 'n1')
        n1 = self.portal['n1']
        n1.setLayout('nitf_galleria')
        self.assertEqual(n1.getLayout(), 'nitf_galleria')

        update_galleria_layout(self.portal)

        self.assertEqual(n1.getLayout(), 'galleria')
