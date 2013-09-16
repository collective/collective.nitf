# -*- coding: utf-8 -*-

from collective.nitf.testing import SELENIUM_TESTING
from plone.testing import layered

import os
import robotsuite
import unittest

dirname = os.path.dirname(__file__)
files = os.listdir(dirname)
tests = [f for f in files if f.startswith('robot_') and f.endswith('.txt')]


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(robotsuite.RobotTestSuite(t), layer=SELENIUM_TESTING)
        for t in tests
    ])
    return suite
