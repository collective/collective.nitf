# -*- coding: utf-8 -*-

from collective.nitf.testing import FUNCTIONAL_TESTING
from plone.testing import layered

import doctest
import os
import unittest


dirname = os.path.dirname(__file__)
files = os.listdir(dirname)
tests = [f for f in files if f.startswith("test_") and f.endswith(".txt")]


# FIXME: Fix test_collection.txt in Plone 5.2
tests = []


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests(
        [layered(doctest.DocFileSuite(t), layer=FUNCTIONAL_TESTING) for t in tests]
    )
    return suite
