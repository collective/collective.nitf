# -*- coding: utf-8 -*-

from collective.nitf.setuphandlers import upgrade_to_1008
from collective.nitf.setuphandlers import upgrade_to_1009
from collective.nitf.testing import INTEGRATION_TESTING
from plone import api
from plone.app.relationfield.behavior import IRelatedItems
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.registry import field
from plone.registry.interfaces import IRegistry
from plone.registry.record import Record
from zope.component import getUtility
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


class UpgradeTestCaseBase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self, from_version, to_version):
        self.portal = self.layer['portal']
        self.setup = self.portal['portal_setup']
        self.profile_id = u'collective.nitf:default'
        self.from_version = from_version
        self.to_version = to_version

    def _get_upgrade_step(self, title):
        """Get upgrade step."""
        self.setup.setLastVersionForProfile(self.profile_id, self.from_version)
        upgrades = self.setup.listUpgrades(self.profile_id)
        steps = [s for s in upgrades[0] if s['title'] == title]
        return steps[0] if steps else None

    def _do_upgrade_step(self, step):
        """Execute an upgrade step."""
        request = self.layer['request']
        request.form['profile_id'] = self.profile_id
        request.form['upgrades'] = [step['id']]
        self.setup.manage_doUpgrades(request=request)

    def _upgrades_to_do(self):
        self.setup.setLastVersionForProfile(self.profile_id, self.from_version)
        upgrades = self.setup.listUpgrades(self.profile_id)
        assert len(upgrades) > 0
        return len(upgrades[0])


class to2000TestCase(UpgradeTestCaseBase):

    def setUp(self):
        UpgradeTestCaseBase.setUp(self, u'1009', u'2000')

    def test_upgrade_to_2000_registrations(self):
        version = self.setup.getLastVersionForProfile(self.profile_id)[0]
        self.assertTrue(version >= self.to_version)
        self.assertEqual(self._upgrades_to_do(), 2)

    def test_character_counter_css_resources(self):
        title = u'Miscellaneous'
        step = self._get_upgrade_step(title)
        self.assertIsNotNone(step)

        csstool = self.portal['portal_css']
        old_css = '++resource++collective.nitf/charcount.css'
        new_css = '++resource++collective.nitf/styles.css'

        # simulate state on previous version
        csstool.registerResource(old_css)
        self.assertIn(old_css, csstool.getResourceIds())
        csstool.unregisterResource(new_css)
        self.assertNotIn(new_css, csstool.getResourceIds())

        # execute upgrade step and verify changes were applied
        self._do_upgrade_step(step)

        self.assertIn(new_css, csstool.getResourceIds())

    def test_character_counter_js_resources(self):
        title = u'Miscellaneous'
        step = self._get_upgrade_step(title)
        self.assertIsNotNone(step)

        jstool = self.portal['portal_javascripts']
        old_js = [
            'characters-count.js',
            '++resource++collective.nitf/nitf_fixes.js',
        ]
        new_js = '++resource++collective.nitf/nitf.js'

        # simulate state on previous version
        for js in old_js:
            jstool.registerResource(js)
            self.assertIn(js, jstool.getResourceIds())
        jstool.unregisterResource(new_js)
        self.assertNotIn(new_js, jstool.getResourceIds())

        # execute upgrade step and verify changes were applied
        self._do_upgrade_step(step)

        for js in old_js:
            self.assertNotIn(js, jstool.getResourceIds())
        self.assertIn(new_js, jstool.getResourceIds())

    def test_character_counter_registry_records_removed(self):
        title = u'Miscellaneous'
        step = self._get_upgrade_step(title)
        self.assertIsNotNone(step)

        registry = getUtility(IRegistry)
        BASE_REGISTRY = 'collective.nitf.controlpanel.INITFCharCountSettings.'
        records = [
            BASE_REGISTRY + 'description_max_chars',
            BASE_REGISTRY + 'description_optimal_chars',
            BASE_REGISTRY + 'show_description_counter',
            BASE_REGISTRY + 'show_title_counter',
            BASE_REGISTRY + 'title_max_chars',
            BASE_REGISTRY + 'title_optimal_chars',
        ]

        # simulate state on previous version
        for r in records:
            registry.records[r] = Record(field.TextLine(title=u'Test'))
            self.assertIn(r, registry)

        # execute upgrade step and verify changes were applied
        self._do_upgrade_step(step)

        for r in records:
            self.assertNotIn(r, registry)

    def test_news_article_registered_views(self):
        title = u'Miscellaneous'
        step = self._get_upgrade_step(title)
        self.assertIsNotNone(step)

        ttool = self.portal['portal_types']
        fti = ttool['collective.nitf.content']

        # simulate state on previous version
        view_methods = list(fti.view_methods)
        view_methods.remove('galleria')
        view_methods.append('nitf_galleria')
        fti.view_methods = tuple(view_methods)
        self.assertEqual(len(fti.view_methods), 2)
        self.assertItemsEqual(fti.view_methods, ['view', 'nitf_galleria'])

        # execute upgrade step and verify changes were applied
        self._do_upgrade_step(step)

        self.assertEqual(len(fti.view_methods), 2)
        self.assertItemsEqual(fti.view_methods, ['view', 'galleria'])

    def test_update_news_articles_layouts(self):
        title = u'Update News Articles layouts'
        step = self._get_upgrade_step(title)
        self.assertIsNotNone(step)

        # create a news article and set the layout to 'nitf_galleria'
        with api.env.adopt_roles(['Manager']):
            folder = api.content.create(self.portal, 'Folder', 'folder')
        n1 = api.content.create(folder, 'collective.nitf.content', 'n1')

        n1.setLayout('nitf_galleria')
        self.assertEqual(n1.getLayout(), 'nitf_galleria')

        # execute upgrade step and verify changes were applied
        self._do_upgrade_step(step)

        self.assertEqual(n1.getLayout(), 'galleria')
