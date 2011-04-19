# -*- coding: utf-8 -*-

from Products.PloneTestCase import ptc
import collective.testcaselayer.ptc

ptc.setupPloneSite()


class IntegrationTestLayer(collective.testcaselayer.ptc.BasePTCLayer):

    def afterSetUp(self):
        # Install the collective.nitf product
        self.addProfile('collective.nitf:default')

Layer = IntegrationTestLayer([collective.testcaselayer.ptc.ptc_layer])
