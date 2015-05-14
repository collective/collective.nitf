# -*- coding: utf-8 -*-
"""Setup of test for the package.

We install collective.cover to test the availibility and features of
the tile included for that package.
"""
from PIL import Image
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.testing import z2
from StringIO import StringIO
from z3c.relationfield import RelationValue
from zope.component import getUtility
from zope.intid.interfaces import IIntIds

import os
import random
import string


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import collective.cover
        self.loadZCML(package=collective.cover)
        import collective.nitf
        self.loadZCML(package=collective.nitf)

    def setUpPloneSite(self, portal):
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
        setRoles(portal, TEST_USER_ID, ['Manager'])
        portal.invokeFactory('collective.nitf.content', 'related')
        portal.invokeFactory('collective.nitf.content', 'n1')
        portal.n1.invokeFactory('Image', 'img1')
        portal.n1.invokeFactory('Image', 'img2')
        portal.n1.invokeFactory('Image', 'img3')
        portal.n1.img1.setImage(generate_jpeg(50, 50))
        portal.n1.img2.setImage(generate_jpeg(50, 50))
        portal.n1.img3.setImage(generate_jpeg(50, 50))
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
