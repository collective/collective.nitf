# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.component import createObject
from zope.component import queryUtility

from plone.app.textfield.value import RichTextValue
from Products.CMFPlone.utils import getToolByName
from plone.dexterity.interfaces import IDexterityFTI

from collective.transmogrifier.transmogrifier import Transmogrifier
from collective.nitf.testing import INTEGRATION_TESTING


def populateContainer(self, container, default_type='News Item', limit=4):
    for n in range(0, limit):
        n_id = 'n%s' % str(n + 1)
        container.invokeFactory(default_type,
                                id=n_id,
                                title=u'News %s' % str(n + 1),
                                description=u'Description %s' % str(n + 1),
                                subject=(u"Category 1", u"Category 2", u"A third category")
                                )
        notify(ObjectAddedEvent(container[n_id]))
        if default_type == 'News Item':
            container[n_id].setText(u'News %s' % str(n + 1))
            # Randomly sets images on news items
            if random.choice([True, False]):
                container[n_id].setImage(StringIO(zptlogo))
                container[n_id].setImageCaption(u'Zope LOGO %s' % str(n + 1))
        if default_type == 'collective.nitf.content':
            container[n_id].body = RichTextValue(u'<p>News %s</p>' % str(n + 1),
                                    'text/html', 'text/x-html-safe')
            #logger.debug(u"Populating: %s %s %s" % (default_type, n_id, container[n_id].objectIds()))
        container[n_id].reindexObject()


class TestNITFIntegration(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def test_transmogrify(self):
        portal = self.layer['portal']
        catalog = getToolByName(portal, 'portal_catalog')
        results = catalog({'portal_type': u'collective.nitf.content', }, )
        self.assertEqual(len(results), 0)
        transmogrifier = Transmogrifier(portal)
        transmogrifier("nitfmigrator")
        results = catalog({'portal_type': u'collective.nitf.content', }, )
        self.assertEqual(len(results), 4)

    def test_migrate_dry_run(self):
        pass


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
