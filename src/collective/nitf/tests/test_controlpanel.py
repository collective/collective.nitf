# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.component import getMultiAdapter
from zope.component import getUtility

from plone.app.testing import TEST_USER_ID
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.registry.interfaces import IRegistry

from collective.nitf.config import PROJECTNAME
from collective.nitf.config import DEFAULT_GENRE, DEFAULT_URGENCY
from collective.nitf.controlpanel import INITFSettings
from collective.nitf.testing import INTEGRATION_TESTING


class ControlPanelTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.controlpanel = self.portal['portal_controlpanel']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_controlpanel_has_view(self):
        view = getMultiAdapter((self.portal, self.portal.REQUEST),
                               name='nitf-settings')
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_controlpanel_view_is_protected(self):
        from AccessControl import Unauthorized
        logout()
        self.assertRaises(Unauthorized,
                          self.portal.restrictedTraverse,
                         '@@nitf-settings')

    def test_controlpanel_installed(self):
        actions = [a.getAction(self)['id']
                   for a in self.controlpanel.listActions()]
        self.assertTrue('nitf' in actions,
                        'control panel was not installed')

    def test_controlpanel_removed_on_uninstall(self):
        qi = self.portal['portal_quickinstaller']
        qi.uninstallProducts(products=[PROJECTNAME])
        actions = [a.getAction(self)['id']
                   for a in self.controlpanel.listActions()]
        self.assertTrue('nitf' not in actions,
                        'control panel was not removed')


class RegistryTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(INITFSettings)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_sections_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'sections'))
        self.assertEqual(self.settings.sections, set([]))

    def test_default_section_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'default_section'))
        self.assertEqual(self.settings.default_section, None)

    def test_default_genre_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'default_genre'))
        self.assertEqual(self.settings.default_genre, DEFAULT_GENRE)

    def test_possible_genres_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'possible_genres'))
        self.assertEqual(self.settings.possible_genres, None)

    def test_default_urgency_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'default_urgency'))
        self.assertEqual(self.settings.default_urgency, DEFAULT_URGENCY)

    def get_record(self, record):
        """ Helper function; it raises KeyError if the record is not in the
        registry.
        """
        prefix = 'collective.nitf.controlpanel.INITFSettings.'
        return self.registry[prefix + record]

    def test_records_removed_on_uninstall(self):
        # XXX: I haven't found a better way to test this; anyone?
        qi = self.portal['portal_quickinstaller']
        qi.uninstallProducts(products=[PROJECTNAME])
        self.assertRaises(KeyError, self.get_record, 'sections')
        self.assertRaises(KeyError, self.get_record, 'default_section')
        self.assertRaises(KeyError, self.get_record, 'default_genre')
        self.assertRaises(KeyError, self.get_record, 'default_urgency')
