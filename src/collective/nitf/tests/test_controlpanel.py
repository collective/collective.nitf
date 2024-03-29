# -*- coding: utf-8 -*-
from collective.nitf.config import DEFAULT_URGENCY
from collective.nitf.config import PROJECTNAME
from collective.nitf.controlpanel import INITFSettings
from collective.nitf.testing import INTEGRATION_TESTING
from plone import api
from plone.app.testing import logout
from plone.registry.interfaces import IRegistry
from Products.CMFPlone.utils import get_installer
from zope.component import getUtility

import unittest


class ControlPanelTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.controlpanel = self.portal["portal_controlpanel"]

    def test_controlpanel_has_view(self):
        request = self.layer["request"]
        view = api.content.get_view(u"nitf-settings", self.portal, request)
        self.assertTrue(view())

    def test_controlpanel_view_is_protected(self):
        from AccessControl import Unauthorized

        logout()
        with self.assertRaises(Unauthorized):
            self.portal.restrictedTraverse("@@nitf-settings")

    def test_site_administrator_can_access_configlet(self):
        with api.env.adopt_roles(["Site Administrator"]):
            self.portal.restrictedTraverse("@@nitf-settings")

    def test_controlpanel_installed(self):
        actions = [a.getAction(self)["id"] for a in self.controlpanel.listActions()]
        self.assertIn("nitf", actions, "control panel not installed")

    def test_controlpanel_removed_on_uninstall(self):
        installer = get_installer(self.portal, self.request)

        with api.env.adopt_roles(["Manager"]):
            installer.uninstall_product(PROJECTNAME)

        actions = [a.getAction(self)["id"] for a in self.controlpanel.listActions()]
        self.assertNotIn("nitf", actions, "control panel not removed")


class RegistryTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(INITFSettings)

    def test_available_sections_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, "available_sections"))
        self.assertEqual(self.settings.available_sections, set([u"General"]))

    def test_default_section_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, "default_section"))
        self.assertEqual(self.settings.default_section, u"General")

    def test_available_genres_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, "available_genres"))
        self.assertEqual(self.settings.available_genres, [u"Current"])

    def test_default_genre_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, "default_genre"))
        self.assertEqual(self.settings.default_genre, u"Current")

    def test_default_urgency_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, "default_urgency"))
        self.assertEqual(self.settings.default_urgency, DEFAULT_URGENCY)

    def test_records_removed_on_uninstall(self):
        installer = get_installer(self.portal, self.request)

        with api.env.adopt_roles(["Manager"]):
            installer.uninstall_product(PROJECTNAME)

        BASE_REGISTRY = "collective.nitf.controlpanel.INITFSettings.{0}"
        records = [
            BASE_REGISTRY.format("available_sections"),
            BASE_REGISTRY.format("default_section"),
            BASE_REGISTRY.format("available_genres"),
            BASE_REGISTRY.format("default_genre"),
            BASE_REGISTRY.format("default_urgency"),
            BASE_REGISTRY.format("relatable_content_types"),
        ]

        for r in records:
            self.assertNotIn(r, self.registry)
