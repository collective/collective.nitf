# -*- coding: utf-8 -*-

from collective.nitf.browser import NITFBylineViewlet
from collective.nitf.testing import INTEGRATION_TESTING
from DateTime import DateTime
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


class NITFBylineViewletTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.workflow_tool = self.portal['portal_workflow']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        self.folder = self.portal['test-folder']

        self.folder.invokeFactory('collective.nitf.content', 'n1')
        self.n1 = self.folder['n1']

    def viewlet(self, context=None):
        context = context or self.portal
        viewlet = NITFBylineViewlet(context, self.request, None, None)
        viewlet.update()
        return viewlet

    def test_pub_date_globally_allowed(self):
        site_properties = self.portal['portal_properties'].site_properties
        if not site_properties.hasProperty('displayPublicationDateInByline'):
            site_properties.manage_addProperty('displayPublicationDateInByline', True, 'boolean')
        site_properties.manage_changeProperties(displayPublicationDateInByline='True')
        viewlet = self.viewlet(self.n1)
        # method must return None as news article has not been published yet
        self.assertIsNone(viewlet.pub_date())

        # we publish the news article and now the method must return a Date
        self.workflow_tool.doActionFor(self.n1, 'publish')
        self.n1.setEffectiveDate(DateTime())
        self.assertIsNotNone(viewlet.pub_date())

    def test_pub_date_not_globally_allowed(self):
        viewlet = self.viewlet(self.n1)
        # method must return None as is not globally allowed
        self.assertIsNone(viewlet.pub_date())

        # we publish the news article and the method must return None also
        self.workflow_tool.doActionFor(self.n1, 'publish')
        self.assertIsNone(viewlet.pub_date())
