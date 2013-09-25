# -*- coding: utf-8 -*-

from collective.nitf.setuphandlers import upgrade_to_1008
from collective.nitf.setuphandlers import upgrade_to_1009
from collective.nitf.testing import INTEGRATION_TESTING
from plone.app.relationfield.behavior import IRelatedItems
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.CMFCore.utils import getToolByName
from zope.component import queryUtility
from zope.intid.interfaces import IIntIds

import unittest


class Upgradeto1008TestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_update_dependencies(self):
        """Test plone.app.relationfield & IIntIds utility were installed.
        """
        qi = self.portal.portal_quickinstaller
        dependencies = ('plone.app.relationfield', 'plone.app.intid')

        # manually uninstall resources to simulate previous profile
        for dependency in dependencies:
            if qi.isProductInstalled(dependency):
                qi.uninstallProducts([dependency])
            self.assertFalse(qi.isProductInstalled(dependency))
        self.assertIsNone(queryUtility(IIntIds))

        # run the upgrade step and test resources are installed
        upgrade_to_1008(self.portal)
        for dependency in dependencies:
            self.assertTrue(qi.isProductInstalled(dependency), msg='{0} not installed'.format(dependency))
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
        ttool = getToolByName(self.portal, 'portal_types')
        fti = ttool['collective.nitf.content']
        self.assertTrue('plone.app.relationfield.behavior.IRelatedItems' in fti.behaviors)

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
        self.assertTrue('plone.app.relationfield.behavior.IRelatedItems' in fti.behaviors)
