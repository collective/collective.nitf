# -*- coding: utf-8 -*-
import random
from StringIO import StringIO
from PIL import Image

from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing.z2 import ZSERVER_FIXTURE
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import collective.nitf
        self.loadZCML(package=collective.nitf)

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'collective.nitf:default')


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
    image = Image.new("RGB", (width, height))
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
    image.save(output, format="PNG")
    return output.getvalue()


class SeleniumFixture(Fixture):

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'collective.nitf:default')
        setRoles(portal, TEST_USER_ID, ['Manager'])
        portal.invokeFactory('collective.nitf.content', 'n1')
        portal.n1.invokeFactory('Image', 'img1')
        portal.n1.invokeFactory('Image', 'img2')
        portal.n1.invokeFactory('Image', 'img3')
        portal.n1.img1.setImage(generate_jpeg(50, 50))
        portal.n1.img2.setImage(generate_jpeg(50, 50))
        portal.n1.img3.setImage(generate_jpeg(50, 50))


FIXTURE = Fixture()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='collective.nitf:Integration',
)
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name='collective.nitf:Functional',
)
SELENIUM_FIXTURE = SeleniumFixture()
SELENIUM_TESTING = FunctionalTesting(
    bases=(SELENIUM_FIXTURE, ZSERVER_FIXTURE),
    name='collective.nitf:Selenium',
)
