# -*- coding: utf-8 -*-
from collective.nitf.testing import ROBOT_TESTING
from plone.testing import layered

import os
import robotsuite
import unittest


files = os.listdir(os.path.dirname(__file__))
tests = [f for f in files if f.startswith("test_") and f.endswith(".robot")]

noncritical = ["Expected Failure"]
# FIXME: https://github.com/collective/collective.nitf/issues/172
noncritical.append("issue_172")

# FIXME: Make RobotFramework tests work in Plone 5
tests = []


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests(
        [
            layered(
                robotsuite.RobotTestSuite(t, noncritical=noncritical),
                layer=ROBOT_TESTING,
            )
            for t in tests
        ]
    )
    return suite
