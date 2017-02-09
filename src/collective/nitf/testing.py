# -*- coding: utf-8 -*-
"""Setup testing infrastructure.

For Plone 5 we need to install plone.app.contenttypes.

Tile for collective.cover is only tested in Plone 4.3.
"""
from plone import api
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2
from z3c.relationfield import RelationValue
from zope.component import getUtility
from zope.intid.interfaces import IIntIds

import os
import pkg_resources
import shutil


try:
    pkg_resources.get_distribution('plone.app.contenttypes')
except pkg_resources.DistributionNotFound:
    from plone.app.testing import PLONE_FIXTURE
    DEXTERITY_ONLY = False
else:
    from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE as PLONE_FIXTURE
    DEXTERITY_ONLY = True

try:
    pkg_resources.get_distribution('collective.cover')
except pkg_resources.DistributionNotFound:
    HAS_COVER = False
else:
    HAS_COVER = True

IS_PLONE_5 = api.env.plone_version().startswith('5')

# set of images to be used on tests
IMAGES = (
    '640px-Mandel_zoom_00_mandelbrot_set.jpg',
    '640px-Mandel_zoom_04_seehorse_tail.jpg',
    '640px-Mandel_zoom_06_double_hook.jpg',
)


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        if HAS_COVER:
            import collective.cover
            self.loadZCML(package=collective.cover)

        import collective.nitf
        self.loadZCML(package=collective.nitf)

    def setUpPloneSite(self, portal):
        if HAS_COVER:
            self.applyProfile(portal, 'collective.cover:default')

        self.applyProfile(portal, 'collective.nitf:default')

        portal.portal_workflow.setDefaultChain('simple_publication_workflow')

        for i in IMAGES:
            origin = os.path.join(os.path.dirname(__file__), 'tests', i)
            shutil.copy2(origin, '/tmp')


def get_image(name):
    image = os.path.join(os.path.dirname(__file__), 'tests', name)
    return open(image).read()


def generate_text(size):
    import random
    import string
    chars = string.letters + string.digits
    return ''.join(random.choice(chars) for x in range(size))


# TODO: simplify this using a testfixture profile
class RobotFixture(Fixture):

    def setUpPloneSite(self, portal):
        super(RobotFixture, self).setUpPloneSite(portal)
        with api.env.adopt_roles(['Manager']):
            api.content.create(portal, 'collective.nitf.content', 'related')
            obj = api.content.create(portal, 'collective.nitf.content', 'n1')

        from collective.nitf.tests.api_hacks import set_image_field
        api.content.create(obj, 'Image', 'img1')
        api.content.create(obj, 'Image', 'img2')
        api.content.create(obj, 'Image', 'img3')
        set_image_field(obj['img1'], get_image(IMAGES[0]), 'image/jpeg')
        set_image_field(obj['img2'], get_image(IMAGES[1]), 'image/jpeg')
        set_image_field(obj['img3'], get_image(IMAGES[2]), 'image/jpeg')
        intids = getUtility(IIntIds)
        to_id = intids.getId(portal.related)
        portal.n1.relatedItems = [RelationValue(to_id)]
        open('/tmp/random.txt', 'w').write(generate_text(256))


FIXTURE = Fixture()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name='collective.nitf:Integration')

FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,), name='collective.nitf:Functional')

ROBOT_FIXTURE = RobotFixture()
ROBOT_TESTING = FunctionalTesting(
    bases=(ROBOT_FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE, z2.ZSERVER_FIXTURE),
    name='collective.nitf:Robot',
)

# first image as a string
FRACTAL = get_image(IMAGES[0])
