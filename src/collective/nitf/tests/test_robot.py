# -*- coding: utf-8 -*-
from collective.nitf.testing import DEXTERITY_ONLY
from collective.nitf.testing import IS_PLONE_5
from collective.nitf.testing import ROBOT_TESTING
from plone.testing import layered

import os
import robotsuite
import unittest


files = os.listdir(os.path.dirname(__file__))
tests = [f for f in files if f.startswith('test_') and f.endswith('.robot')]

noncritical = ['Expected Failure']
if DEXTERITY_ONLY:
    # FIXME: https://github.com/collective/collective.nitf/issues/172
    noncritical.append('issue_172')

# skip RobotFramework tests in Plone 5
if IS_PLONE_5:
    tests = []


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(
            robotsuite.RobotTestSuite(t, noncritical=noncritical),
            layer=ROBOT_TESTING)
        for t in tests
    ])
    return suite
