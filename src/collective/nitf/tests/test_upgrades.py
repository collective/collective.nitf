# -*- coding: utf-8 -*-

from collective.nitf.setuphandlers import upgrade_to_1008
from collective.nitf.testing import INTEGRATION_TESTING
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
