# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.component import getMultiAdapter
from zope.component import getUtility

from plone.app.testing import TEST_USER_ID
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.registry import Registry
from plone.registry.interfaces import IRegistry

from Products.CMFCore.utils import getToolByName

from collective.nitf import config
from collective.nitf.controlpanel import INITFSettings
from collective.nitf.testing import INTEGRATION_TESTING


class RegistryTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        # Set up the NITF settings registry
        self.registry = Registry()
        self.registry.registerInterface(INITFSettings)

    def test_nitf_controlpanel_view(self):
        # Test the NITF setting control panel view
        view = getMultiAdapter((self.portal, self.portal.REQUEST),
                               name=config.CONTROLPANEL_ID)
        view = view.__of__(self.portal)
        self.failUnless(view())

    def test_nitf_controlpanel_view_protected(self):
        # Test that the NITF setting control panel view can not be accessed
        # by anonymous users
        from AccessControl import Unauthorized
        logout()
        self.assertRaises(Unauthorized,
                          self.portal.restrictedTraverse,
                         '@@nitf-settings')

    def test_nitf_in_controlpanel(self):
        # Check that there is an NITF entry in the control panel
        self.controlpanel = getToolByName(self.portal, 'portal_controlpanel')
        self.failUnless('nitf' in [a.getAction(self)['id']
                            for a in self.controlpanel.listActions()])

    def test_record_sections(self):
        # Test that the sections record is in the control panel
        record_sections = self.registry.records[
            'collective.nitf.controlpanel.INITFSettings.sections']
        self.failUnless('sections' in INITFSettings)
        self.assertEquals(record_sections.value, set([]))

    def test_record_default_section(self):
        # Test that the default_section record is in the control panel
        record_default_section = self.registry.records[
            'collective.nitf.controlpanel.INITFSettings.default_section']
        self.failUnless('default_section' in INITFSettings)
        self.assertEquals(record_default_section.value, None)

    def test_record_default_genre(self):
        # Test that the default_genre record is in the control panel
        record_default_genre = self.registry.records[
            'collective.nitf.controlpanel.INITFSettings.default_genre']
        self.failUnless('default_genre' in INITFSettings)
        self.assertEquals(record_default_genre.value,
                          config.DEFAULT_GENRE)

    def test_record_default_urgency(self):
        # Test that the default_urgency record is in the control panel
        record_default_urgency = self.registry.records[
            'collective.nitf.controlpanel.INITFSettings.default_urgency']
        self.failUnless('default_urgency' in INITFSettings)
        self.assertEquals(record_default_urgency.value,
                          config.DEFAULT_URGENCY)

    def test_javascript_registry_configured(self):
        portal = self.layer['portal']
        jsRegistry = getToolByName(portal, 'portal_javascripts')
        self.assertTrue("++resource++collective.nitf/nitf_fixes.js"
            in jsRegistry.getResourceIds())
        self.assertTrue("++resource++collective.nitf/jquery.collapsible-v.2.1.3.js"
            in jsRegistry.getResourceIds())
    
    def test_css_registry_configured(self):
        portal = self.layer['portal']
        cssRegistry = getToolByName(portal, 'portal_css')
        self.assertTrue("++resource++collective.nitf/collapsible.css"
            in cssRegistry.getResourceIds())

from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login


class RegistryUninstallTest(unittest.TestCase):
    """ensure registry is properly uninstalled"""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.registry = getUtility(IRegistry)
        # uninstall the package
        self.qi = getattr(self.portal, 'portal_quickinstaller')
        self.qi.uninstallProducts(products=[config.PROJECTNAME])

    def test_javascript_registry_configured(self):
        portal = self.layer['portal']
        jsRegistry = getToolByName(portal, 'portal_javascripts')
        self.assertTrue("++resource++collective.nitf/nitf_fixes.js"
            not in jsRegistry.getResourceIds())
        self.assertTrue("++resource++collective.nitf/jquery.collapsible-v.2.1.3.js"
            not in jsRegistry.getResourceIds())

    def test_css_registry_configured(self):
        portal = self.layer['portal']
        cssRegistry = getToolByName(portal, 'portal_css')
        self.assertTrue("++resource++collective.nitf/collapsible.css"
            not in cssRegistry.getResourceIds())

    def test_records_uninstalled(self):
        # Test that the records were removed from the control panel
        records = [
            'collective.nitf.controlpanel.INITFSettings.sections',
            'collective.nitf.controlpanel.INITFSettings.default_section',
            'collective.nitf.controlpanel.INITFSettings.default_genre',
            'collective.nitf.controlpanel.INITFSettings.default_urgency',
            ]
        for r in records:
            self.failIf(r in self.registry)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
