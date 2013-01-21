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
        try:
            import collective.syndication
            self.loadZCML(package=collective.syndication)
        except:
            # No collective.syndication
            pass

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        try:
            self.applyProfile(portal, 'collective.syndication:default')
        except:
            # No collective.syndication
            pass
        self.applyProfile(portal, 'collective.nitf:default')
        
        wf = getattr(portal, 'portal_workflow')
        types = ('collective.nitf.content', )
        wf.setChainForPortalTypes(types, 'simple_publication_workflow')


FIXTURE = Fixture()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='collective.nitf:Integration',
)
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name='collective.nitf:Functional',
)
