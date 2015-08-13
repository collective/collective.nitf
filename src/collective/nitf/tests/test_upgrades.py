# -*- coding: utf-8 -*-
from collective.nitf.testing import INTEGRATION_TESTING
from plone import api
from plone.registry import field
from plone.registry.interfaces import IRegistry
from plone.registry.record import Record
from zope.component import getUtility

import unittest


class UpgradeTestCaseBase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self, from_version, to_version):
        self.portal = self.layer['portal']
        self.setup = self.portal['portal_setup']
        self.profile_id = u'collective.nitf:default'
        self.from_version = from_version
        self.to_version = to_version

    def get_upgrade_step(self, title):
        """Get the named upgrade step."""
        self.setup.setLastVersionForProfile(self.profile_id, self.from_version)
        upgrades = self.setup.listUpgrades(self.profile_id)
        steps = [s for s in upgrades[0] if s['title'] == title]
        return steps[0] if steps else None

    def execute_upgrade_step(self, step):
        """Execute an upgrade step."""
        request = self.layer['request']
        request.form['profile_id'] = self.profile_id
        request.form['upgrades'] = [step['id']]
        self.setup.manage_doUpgrades(request=request)

    @property
    def total_steps(self):
        """Return the number of steps in the upgrade."""
        self.setup.setLastVersionForProfile(self.profile_id, self.from_version)
        upgrades = self.setup.listUpgrades(self.profile_id)
        assert len(upgrades) > 0
        return len(upgrades[0])


class to1007TestCase(UpgradeTestCaseBase):

    def setUp(self):
        UpgradeTestCaseBase.setUp(self, u'1006', u'1007')

    def test_upgrade_to_2000_registrations(self):
        version = self.setup.getLastVersionForProfile(self.profile_id)[0]
        self.assertTrue(version >= self.to_version)
        self.assertEqual(self.total_steps, 1)

    def test_add_locking_behavior(self):
        title = u'Add locking behavior'
        step = self.get_upgrade_step(title)
        self.assertIsNotNone(step)

        locking_behavior = 'plone.app.lockingbehavior.behaviors.ILocking'
        types = self.portal['portal_types']
        nitf = types['collective.nitf.content']

        # simulate state on previous version
        behaviors = list(nitf.behaviors)
        behaviors.remove(locking_behavior)
        nitf.behaviors = tuple(behaviors)
        self.assertNotIn(locking_behavior, nitf.behaviors)

        # execute upgrade step and verify changes were applied
        self.execute_upgrade_step(step)

        self.assertIn(locking_behavior, nitf.behaviors)


class to2000TestCase(UpgradeTestCaseBase):

    def setUp(self):
        UpgradeTestCaseBase.setUp(self, u'1008', u'2000')

    def test_upgrade_to_2000_registrations(self):
        version = self.setup.getLastVersionForProfile(self.profile_id)[0]
        self.assertTrue(version >= self.to_version)
        self.assertEqual(self.total_steps, 4)

    def test_character_counter_css_resources(self):
        title = u'Miscellaneous'
        step = self.get_upgrade_step(title)
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
        self.execute_upgrade_step(step)

        self.assertIn(new_css, csstool.getResourceIds())

    def test_character_counter_js_resources(self):
        title = u'Miscellaneous'
        step = self.get_upgrade_step(title)
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
        self.execute_upgrade_step(step)

        for js in old_js:
            self.assertNotIn(js, jstool.getResourceIds())
        self.assertIn(new_js, jstool.getResourceIds())

    def test_character_counter_registry_records_removed(self):
        title = u'Miscellaneous'
        step = self.get_upgrade_step(title)
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
        self.execute_upgrade_step(step)

        for r in records:
            self.assertNotIn(r, registry)

    def test_news_article_registered_views(self):
        title = u'Miscellaneous'
        step = self.get_upgrade_step(title)
        self.assertIsNotNone(step)

        ttool = self.portal['portal_types']
        fti = ttool['collective.nitf.content']

        # simulate state on previous version
        view_methods = list(fti.view_methods)
        view_methods.remove('slideshow_view')
        view_methods.remove('text_only_view')
        view_methods.append('nitf_galleria')
        fti.view_methods = tuple(view_methods)
        self.assertEqual(len(fti.view_methods), 2)
        self.assertItemsEqual(fti.view_methods, ['view', 'nitf_galleria'])

        # execute upgrade step and verify changes were applied
        self.execute_upgrade_step(step)

        self.assertEqual(len(fti.view_methods), 3)
        self.assertItemsEqual(
            fti.view_methods, ['view', 'slideshow_view', 'text_only_view'])

    def test_update_news_articles_layouts(self):
        title = u'Update News Articles layouts'
        step = self.get_upgrade_step(title)
        self.assertIsNotNone(step)

        # create a news article and set the layout to 'nitf_galleria'
        with api.env.adopt_roles(['Manager']):
            folder = api.content.create(self.portal, 'Folder', 'folder')
        n1 = api.content.create(folder, 'collective.nitf.content', 'n1')

        n1.setLayout('nitf_galleria')
        self.assertEqual(n1.getLayout(), 'nitf_galleria')

        # execute upgrade step and verify changes were applied
        self.execute_upgrade_step(step)

        self.assertEqual(n1.getLayout(), 'slideshow_view')

    def test_install_new_dependencies(self):
        # check if the upgrade step is registered
        title = u'Install new dependencies'
        step = self.get_upgrade_step(title)
        self.assertIsNotNone(step)

        # simulate state on previous version
        dependencies = ('collective.js.cycle2',)
        qi = api.portal.get_tool('portal_quickinstaller')
        qi.uninstallProducts(dependencies)
        for p in dependencies:
            self.assertFalse(qi.isProductInstalled(p))

        # execute upgrade step and verify changes were applied
        self.execute_upgrade_step(step)

        for p in dependencies:
            self.assertTrue(qi.isProductInstalled(p))

    def test_update_configlet(self):
        # check if the upgrade step is registered
        title = u'Update control panel configlet'
        step = self.get_upgrade_step(title)
        self.assertIsNotNone(step)

        # simulate state on previous version
        cptool = api.portal.get_tool('portal_controlpanel')
        configlet = cptool.getActionObject('Products/nitf')
        configlet.permissions = old_permissions = ('cmf.ManagePortal',)
        self.assertEqual(configlet.getPermissions(), old_permissions)

        # run the upgrade step to validate the update
        self.execute_upgrade_step(step)
        configlet = cptool.getActionObject('Products/nitf')
        new_permissions = ('collective.nitf: Setup',)
        self.assertEqual(configlet.getPermissions(), new_permissions)
