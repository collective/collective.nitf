# -*- coding: utf-8 -*-

from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import collective.nitf
        self.loadZCML(package=collective.nitf)

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'collective.nitf:default')


FIXTURE = Fixture()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='collective.nitf:Integration',
)
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name='collective.nitf:Functional',
)
