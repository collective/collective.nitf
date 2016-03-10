# -*- coding: utf-8 -*-
"""Setup of test for the package.

We install collective.cover to test the availibility and features of
the tile included for that package.

For Plone 5 we need to install plone.app.contenttypes.
"""
from PIL import Image
from plone import api
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2
from StringIO import StringIO
from z3c.relationfield import RelationValue
from zope.component import getUtility
from zope.intid.interfaces import IIntIds

import os
import pkg_resources
import random
import string


try:
    pkg_resources.get_distribution('plone.app.contenttypes')
except pkg_resources.DistributionNotFound:
    from plone.app.testing import PLONE_FIXTURE
else:
    from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE as PLONE_FIXTURE


PLONE_VERSION = api.env.plone_version()


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # XXX: avoid import issues with collective.cover < 1.0a13
        if PLONE_VERSION.startswith('5'):
            import Products.Archetypes
            self.loadZCML(package=Products.Archetypes)
        else:
            import collective.cover
            self.loadZCML(package=collective.cover)
        import collective.nitf
        self.loadZCML(package=collective.nitf)

    def setUpPloneSite(self, portal):
        # XXX: avoid import issues with collective.cover < 1.0a13
        if PLONE_VERSION.startswith('5'):
            from plone.app.testing import quickInstallProduct
            quickInstallProduct(portal, 'Products.Archetypes')
        else:
            self.applyProfile(portal, 'collective.cover:default')

        self.applyProfile(portal, 'collective.nitf:default')

        portal_workflow = portal['portal_workflow']
        portal_workflow.setChainForPortalTypes(
            ('collective.nitf.content',), 'simple_publication_workflow')


def generate_jpeg(width, height):
    # Mandelbrot fractal
    # FB - 201003254
    # drawing area
    xa = -2.0
    xb = 1.0
    ya = -1.5
    yb = 1.5
    maxIt = 25  # max iterations allowed
    # image size
    image = Image.new('RGB', (width, height))
    c = complex(random.random() * 2.0 - 1.0, random.random() - 0.5)

    for y in range(height):
        zy = y * (yb - ya) / (height - 1) + ya
        for x in range(width):
            zx = x * (xb - xa) / (width - 1) + xa
            z = complex(zx, zy)
            for i in range(maxIt):
                if abs(z) > 2.0:
                    break
                z = z * z + c
            r = i % 4 * 64
            g = i % 8 * 32
            b = i % 16 * 16
            image.putpixel((x, y), b * 65536 + g * 256 + r)

    output = StringIO()
    image.save(output, format='PNG')
    return output.getvalue()


def generate_text(size):
    chars = string.letters + string.digits
    return ''.join(random.choice(chars) for x in range(size))


# TODO: simplify this using a testfixture profile
class RobotFixture(Fixture):

    def setUpPloneSite(self, portal):
        super(RobotFixture, self).setUpPloneSite(portal)
        with api.env.adopt_roles(['Manager']):
            api.content.create(
                portal, 'collective.nitf.content', 'related')
            api.content.create(
                portal, 'collective.nitf.content', 'n1')

        from collective.nitf.tests.api_hacks import set_image_field
        portal.n1.invokeFactory('Image', 'img1')
        portal.n1.invokeFactory('Image', 'img2')
        portal.n1.invokeFactory('Image', 'img3')
        set_image_field(portal['img1'], generate_jpeg(50, 50), 'image/png')
        set_image_field(portal['img2'], generate_jpeg(50, 50), 'image/png')
        set_image_field(portal['img3'], generate_jpeg(50, 50), 'image/png')
        intids = getUtility(IIntIds)
        to_id = intids.getId(portal.related)
        portal.n1.relatedItems = [RelationValue(to_id), ]
        open('/tmp/img1.jpg', 'w').write(generate_jpeg(50, 50))
        open('/tmp/txt1.txt', 'w').write(generate_text(256))

    def tearDownPloneSite(self, portal):
        os.remove('/tmp/img1.jpg')
        os.remove('/tmp/txt1.txt')


FIXTURE = Fixture()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='collective.nitf:Integration',
)

FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name='collective.nitf:Functional',
)

ROBOT_FIXTURE = RobotFixture()
ROBOT_TESTING = FunctionalTesting(
    bases=(ROBOT_FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE, z2.ZSERVER_FIXTURE),
    name='collective.nitf:Robot',
)
