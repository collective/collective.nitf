# -*- coding: utf-8 -*-

from Products.PloneTestCase import ptc
import collective.testcaselayer.ptc

ptc.setupPloneSite()


class IntegrationTestLayer(collective.testcaselayer.ptc.BasePTCLayer):

    def afterSetUp(self):
        # Install the collective.nitf product
        self.addProfile('collective.nitf:default')

Layer = IntegrationTestLayer([collective.testcaselayer.ptc.ptc_layer])


class MigrationTestLayer(collective.testcaselayer.ptc.BasePTCLayer):

    def afterSetUp(self):
        # Install the collective.nitf product
        self.addProfile('collective.nitf:default')
        self.loginAsPortalOwner()
        self.folder.invokeFactory('News Item', 'n1')
        self.folder.invokeFactory('News Item', 'n2')
        self.folder.invokeFactory('News Item', 'n3')
        self.folder.invokeFactory('News Item', 'n4')

        self.folder['n1'].setTitle('News 1')
        self.folder['n1'].setDescription('Description 1')
        self.folder['n1'].setText('News one')
        
        self.folder['n2'].setTitle('News 2')
        self.folder['n2'].setDescription('Description 2')
        self.folder['n2'].setText('News two')
   
        self.folder['n3'].setTitle('News 3')
        self.folder['n3'].setDescription('Description 3')
        self.folder['n3'].setText('News three')
        
        self.folder['n4'].setTitle('News 4')
        self.folder['n4'].setDescription('Description 4')
        self.folder['n4'].setText('News four')
     
        self.portal._delObject('front-page')

MigrationLayer = MigrationTestLayer([collective.testcaselayer.ptc.ptc_layer])

