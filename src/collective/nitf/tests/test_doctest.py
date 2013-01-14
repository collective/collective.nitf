# -*- coding: utf-8 -*-

from collective.nitf.testing import FUNCTIONAL_TESTING
from plone.testing import layered

import doctest
import unittest2 as unittest

# XXX: we must replace this tests with a Robot Framework ones
optionflags = doctest.SKIP


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(doctest.DocFileSuite('tests/functional.txt',
                                     optionflags=optionflags,
                                     package='collective.nitf'),
                layer=FUNCTIONAL_TESTING),
        layered(doctest.DocFileSuite('tests/collection.txt',
                                     package='collective.nitf'),
                layer=FUNCTIONAL_TESTING)
    ])
    return suite
