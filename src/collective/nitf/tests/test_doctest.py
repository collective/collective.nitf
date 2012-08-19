# -*- coding: utf-8 -*-

import unittest2 as unittest
import doctest

from plone.testing import layered

from collective.nitf.testing import FUNCTIONAL_TESTING

# XXX: we must replace this tests with a Robot Framework ones
optionflags = doctest.SKIP


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(doctest.DocFileSuite('tests/functional.txt',
                                     optionflags=optionflags,
                                     package='collective.nitf'),
                layer=FUNCTIONAL_TESTING),
        ])
    return suite
