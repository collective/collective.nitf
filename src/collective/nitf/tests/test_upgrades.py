# -*- coding: utf-8 -*-
from collective.nitf.testing import INTEGRATION_TESTING

import unittest


class UpgradeTestCaseBase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self, from_version, to_version):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]

        self.setup = self.portal["portal_setup"]
        self.profile_id = u"collective.nitf:default"
        self.from_version = from_version
        self.to_version = to_version

    def get_upgrade_step(self, title):
        """Get the named upgrade step."""
        self.setup.setLastVersionForProfile(self.profile_id, self.from_version)
        upgrades = self.setup.listUpgrades(self.profile_id)
        steps = [s for s in upgrades[0] if s["title"] == title]
        return steps[0] if steps else None

    def execute_upgrade_step(self, step):
        """Execute an upgrade step."""
        self.request.form["profile_id"] = self.profile_id
        self.request.form["upgrades"] = [step["id"]]
        self.setup.manage_doUpgrades(request=self.request)

    @property
    def total_steps(self):
        """Return the number of steps in the upgrade."""
        self.setup.setLastVersionForProfile(self.profile_id, self.from_version)
        upgrades = self.setup.listUpgrades(self.profile_id)
        self.assertGreater(len(upgrades), 0)
        return len(upgrades[0])


# FIXME: This class is just an example of an upgrade step test.
# Must be removed when a first test is created.
class to3000TestCase(UpgradeTestCaseBase):
    def setUp(self):
        UpgradeTestCaseBase.setUp(self, u"2000", u"3000")

    def test_upgrade_step_1(self):
        pass

    # def test_upgrade_to_3000_registrations(self):
    #     version = self.setup.getLastVersionForProfile(self.profile_id)[0]
    #     self.assertTrue(version >= self.to_version)
    #     self.assertEqual(self.total_steps, 1)

    # def test_upgrade2(self):
    #     title = u"Upgrade 2"
    #     step = self.get_upgrade_step(title)
    #     self.assertIsNotNone(step)
