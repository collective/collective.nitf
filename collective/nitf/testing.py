# -*- coding: utf-8 -*-

"""
$Id$
"""

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting


class MyProduct(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import collective.nitf
        self.loadZCML(package=collective.nitf)

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'collective.nitf:default')


NITF_FIXTURE = MyProduct()
NITF_INTEGRATION_TESTING = IntegrationTesting(bases=(NITF_FIXTURE,),
                                              name="NITF:Integration")
NITF_FUNCTIONAL_TESTING = FunctionalTesting(bases=(NITF_FIXTURE,),
                                            name="NITF:Functional")
