# -*- coding: utf-8 -*-

from collective.nitf.browser import NITFBylineViewlet
from collective.nitf.testing import INTEGRATION_TESTING
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from DateTime import DateTime
from AccessControl import Unauthorized

import pkg_resources
import unittest2 as unittest

PLONE_VERSION = pkg_resources.require("Plone")[0].version


class NITFBylineViewletTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        self.folder = self.portal['test-folder']

        self.folder.invokeFactory('collective.nitf.content', 'n1')
        self.n1 = self.folder['n1']

    def publish(self, context):
        """Based on: https://github.com/plone/Products.CMFPlone/blob/master/Products/CMFPlone/skins/plone_form_scripts/content_status_modify.cpy
        """
        workflow_action = 'publish'
        effective_date=None
        expiration_date=None
        contentEditSuccess = 0

        new_context = context.portal_factory.doCreate(context)
        portal_workflow = new_context.portal_workflow
        transitions = portal_workflow.getTransitionsFor(new_context)
        transition_ids = [t['id'] for t in transitions]

        if (workflow_action in transition_ids  and
            not effective_date                 and
            context.EffectiveDate() =='None'):
            effective_date = DateTime()

        def editContent(obj,
                        effective,
                        expiry):
            kwargs = {}
            # may contain the year
            if (effective                        and
                (isinstance(effective, DateTime) or
                 len(effective) > 5)):
                kwargs['effective_date'] = effective
            # may contain the year
            if (expiry                        and
                (isinstance(expiry, DateTime) or
                 len(expiry) > 5)):
                kwargs['expiration_date'] = expiry
            new_context.plone_utils.contentEdit(obj, **kwargs)

        #You can transition content but not have the permission to ModifyPortalContent
        try:
            editContent(new_context, effective_date, expiration_date)
            contentEditSuccess = 1
        except Unauthorized:
            pass

        wfcontext = context

        if workflow_action in transition_ids:
            wfcontext = new_context.portal_workflow.doActionFor(context,
                                                                workflow_action,
                                                                comment='')
        if not wfcontext:
            wfcontext = new_context

        #The object post-transition could now have ModifyPortalContent permission.
        if not contentEditSuccess:
            try:
                editContent(wfcontext, effective_date, expiration_date)
            except Unauthorized:
                pass

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
        self.publish(self.n1)
        self.assertIsNotNone(viewlet.pub_date())

    def test_pub_date_not_globally_allowed(self):
        viewlet = self.viewlet(self.n1)
        # method must return None as is not globally allowed
        self.assertIsNone(viewlet.pub_date())

        # we publish the news article and the method must return None also
        self.publish(self.n1)
        self.assertIsNone(viewlet.pub_date())
