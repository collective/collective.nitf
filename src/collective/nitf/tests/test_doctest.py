# -*- coding: utf-8 -*-

import unittest2 as unittest
import doctest

from plone.testing import layered

from collective.nitf.testing import FUNCTIONAL_TESTING

optionflags = doctest.REPORT_ONLY_FIRST_FAILURE


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(doctest.DocFileSuite('functional.txt',
                                     optionflags=optionflags),
                layer=FUNCTIONAL_TESTING),
        doctest.DocTestSuite(module='collective.nitf'),
    ])
    return suite
