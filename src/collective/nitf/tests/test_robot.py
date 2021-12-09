# -*- coding: utf-8 -*-
from collective.nitf.testing import ROBOT_TESTING
from plone.testing import layered

import os
import robotsuite
import unittest


files = os.listdir(os.path.dirname(__file__))
tests = [f for f in files if f.startswith("test_") and f.endswith(".robot")]


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests(
        [
            layered(
                robotsuite.RobotTestSuite(t),
                layer=ROBOT_TESTING,
            )
            for t in tests
        ]
    )
    return suite
