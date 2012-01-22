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

BASE_REGISTRY = 'collective.nitf.controlpanel.INITFSettings.%s'


class RegistryTest(unittest.TestCase):
    """Ensure the NITF registry is properly installed.
    """

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.registry = Registry()
        self.registry.registerInterface(INITFSettings)

    def test_nitf_controlpanel_view(self):
        """The NITF setting control panel must have view.
        """
        view = getMultiAdapter((self.portal, self.portal.REQUEST),
                               name=config.CONTROLPANEL_ID)
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_nitf_controlpanel_view_protected(self):
        """The NITF setting control panel view can not be accessed by
        anonymous users.
        """
        from AccessControl import Unauthorized
        logout()
        self.assertRaises(Unauthorized,
                          self.portal.restrictedTraverse,
                         '@@nitf-settings')

    def test_nitf_in_controlpanel(self):
        """There must be an NITF entry in the control panel.
        """
        self.controlpanel = getToolByName(self.portal, 'portal_controlpanel')
        self.assertTrue('nitf' in [a.getAction(self)['id']
                            for a in self.controlpanel.listActions()])

    def test_record_sections(self):
        """The sections record must be in the control panel.
        """
        record_sections = self.registry.records[
            BASE_REGISTRY % 'sections']
        self.assertTrue('sections' in INITFSettings)
        self.assertEquals(record_sections.value, set([]))

    def test_record_default_section(self):
        """The default section record must be in the control panel.
        """
        record_default_section = self.registry.records[
            BASE_REGISTRY % 'default_section']
        self.assertTrue('default_section' in INITFSettings)
        self.assertEquals(record_default_section.value, None)

    def test_record_default_genre(self):
        """The default genre record must be in the control panel.
        """
        record_default_genre = self.registry.records[
            BASE_REGISTRY % 'default_genre']
        self.assertTrue('default_genre' in INITFSettings)
        self.assertEquals(record_default_genre.value,
                          config.DEFAULT_GENRE)

    def test_record_default_urgency(self):
        """The default urgency record must be in the control panel.
        """
        record_default_urgency = self.registry.records[
            BASE_REGISTRY % 'default_urgency']
        self.assertTrue('default_urgency' in INITFSettings)
        self.assertEquals(record_default_urgency.value,
                          config.DEFAULT_URGENCY)


class RegistryUninstallTest(unittest.TestCase):
    """Ensure the NITF registry is properly uninstalled.
    """

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.registry = getUtility(IRegistry)
        qi = getattr(self.portal, 'portal_quickinstaller')
        qi.uninstallProducts(products=[config.PROJECTNAME])

    def test_records_removed(self):
        """The NITF records must be removed from the registry.
        """
        records = [
            BASE_REGISTRY % 'sections',
            BASE_REGISTRY % 'default_section',
            BASE_REGISTRY % 'default_genre',
            BASE_REGISTRY % 'default_urgency',
            ]
        for r in records:
            self.assertFalse(r in self.registry)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
