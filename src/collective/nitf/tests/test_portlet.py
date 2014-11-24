# -*- coding: utf-8 -*-
from collective.nitf.controlpanel import INITFSettings
from collective.nitf.portlets import latest_sectionable_nitf
from collective.nitf.testing import INTEGRATION_TESTING
from DateTime import DateTime
from plone import api
from plone.app.portlets.storage import PortletAssignmentMapping
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletRenderer
from plone.portlets.interfaces import IPortletType
from plone.registry.interfaces import IRegistry
from zope.component import getMultiAdapter
from zope.component import getUtility

import unittest


class PortletTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_portlet_type_registered(self):
        name = 'collective.nitf.LatestSectionableNITFPortlet'
        latest_sectionable = getUtility(IPortletType, name=name)
        self.assertEqual(latest_sectionable.addview, name)

    def test_interfaces(self):
        last_sectionable = latest_sectionable_nitf.Assignment()
        self.assertTrue(IPortletAssignment.providedBy(last_sectionable))
        self.assertTrue(IPortletDataProvider.providedBy(last_sectionable.data))

    def test_invoke_add_view(self):
        name = 'collective.nitf.LatestSectionableNITFPortlet'
        latest_sectionable = getUtility(IPortletType, name=name)
        path = '++contextportlets++plone.leftcolumn'
        mapping = self.portal.restrictedTraverse(path)

        for m in mapping.keys():
            del mapping[m]

        addview = mapping.restrictedTraverse('+/' + latest_sectionable.addview)
        addview.createAndAdd(data={})

        self.assertEqual(len(mapping), 1)
        self.assertTrue(isinstance(mapping.values()[0],
                                   latest_sectionable_nitf.Assignment))

    def test_invoke_edit_view(self):
        mapping = PortletAssignmentMapping()
        request = self.request

        mapping['latest_nitf'] = latest_sectionable_nitf.Assignment()

        editview = getMultiAdapter((mapping['latest_nitf'], request),
                                   name='edit')
        self.assertTrue(isinstance(editview, latest_sectionable_nitf.EditForm))

    def test_obtain_renderer(self):
        context = self.portal
        request = self.request
        view = context.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager, name='plone.rightcolumn',
                             context=self.portal)

        assgmnt1 = latest_sectionable_nitf.Assignment()

        renderer1 = getMultiAdapter(
            (context, request, view, manager, assgmnt1), IPortletRenderer)

        self.assertTrue(isinstance(renderer1,
                                   latest_sectionable_nitf.Renderer))


class RenderTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def set_default_workflow(self):
        # setup default workflow in tests
        types = ('collective.nitf.content',)
        self.wf.setChainForPortalTypes(types, 'simple_publication_workflow')

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.catalog = self.portal.portal_catalog
        self.wf = self.portal.portal_workflow

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        self.folder = self.portal['test-folder']

        self.set_default_workflow()
        # Let's create 3 sections in the registry
        registry = getUtility(IRegistry)
        settings = registry.forInterface(INITFSettings)
        settings.available_sections = set([u'Section 1',
                                           u'Section 2',
                                           u'Section 3'])

        # Let's create 15 nitf's for each of 3 different sections
        for index in range(1, 16):
            self.folder.invokeFactory('collective.nitf.content',
                                      'section1-nitf-%s' % index)
            n = self.folder['section1-nitf-%s' % index]
            n.title = 'Section 1 Nitf %s' % index
            n.section = 'Section 1'
            n.genre = 'Genre %s' % index
            n.created = DateTime('%(year)s/1/%(index)s %(index)s:00:00' %
                                 {'year': DateTime().year(),
                                  'index': index})
            n.reindexObject()
            # After 5 indexes, publish
            if index % 5 == 0:
                self.wf.doActionFor(n, 'publish')

            self.folder.invokeFactory('collective.nitf.content',
                                      'section2-nitf-%s' % index)
            n = self.folder['section2-nitf-%s' % index]
            n.title = 'Section 2 Nitf %s' % index
            n.section = 'Section 2'
            n.genre = 'Genre %s' % index
            n.created = DateTime('%(year)s/2/%(index)s %(index)s:00:00' %
                                 {'year': DateTime().year(),
                                  'index': index})
            n.reindexObject()
            # After 5 indexes, publish
            if index % 5 == 0:
                self.wf.doActionFor(n, 'publish')

            self.folder.invokeFactory('collective.nitf.content',
                                      'section3-nitf-%s' % index)
            n = self.folder['section3-nitf-%s' % index]
            n.title = 'Section 3 Nitf %s' % index
            n.section = 'Section 3'
            n.genre = 'Genre %s' % index
            n.created = DateTime('%(year)s/3/%(index)s %(index)s:00:00' %
                                 {'year': DateTime().year(),
                                  'index': index})

            n.reindexObject()
            # After 5 indexes, publish
            if index % 5 == 0:
                self.wf.doActionFor(n, 'publish')

        self.default_query = {'Type': ('News Article',),
                              'sort_on': 'created',
                              'sort_order': 'reverse',
                              'sort_limit': 10}

    def renderer(self, context=None, request=None, view=None, manager=None,
                 assignment=None):
        context = context or self.portal
        request = request or self.request
        view = view or self.portal.restrictedTraverse('@@plone')
        manager = manager or getUtility(
            IPortletManager, name='plone.rightcolumn', context=self.portal)

        return getMultiAdapter((context, request, view, manager, assignment),
                               IPortletRenderer)

    def test_render(self):

        assgmnt1 = latest_sectionable_nitf.Assignment()

        r1 = self.renderer(context=self.portal,
                           assignment=assgmnt1)

        r1 = r1.__of__(self.portal)
        r1.update()

    def test_default_search_for_nitf(self):
        assgmnt1 = latest_sectionable_nitf.Assignment()

        r1 = self.renderer(context=self.portal,
                           assignment=assgmnt1)

        r1 = r1.__of__(self.portal)

        view = api.content.get_view(u'nitf-filter-list', r1, self.request)
        results = view.getResults()

        self.assertEqual(len(results), 10)
        query = self.default_query

        catalog_results = self.catalog(**query)[:10]

        self.assertEqual([i.id for i in results],
                         [i.id for i in catalog_results])

        results = view.getResults(limit=45)

        self.assertEqual(len(results), 45)

        query = self.default_query
        query['sort_limit'] = 45

        catalog_results = self.catalog(**query)[:45]

        self.assertEqual([i.id for i in results],
                         [i.id for i in catalog_results])

    def test_filter_sections(self):
        assgmnt1 = latest_sectionable_nitf.Assignment()

        r1 = self.renderer(context=self.portal,
                           assignment=assgmnt1)

        r1 = r1.__of__(self.portal)

        view = api.content.get_view(u'nitf-filter-list', r1, self.request)

        for section in [('section 1', 'Section 1'),
                        ('section 2', 'Section 2'),
                        ('section 3', 'Section 3')]:
            results = view.getResults(section=section[0], limit=45)

            self.assertEqual(len(results), 15)
            query = self.default_query
            query['sort_limit'] = 45
            query['section'] = section[1]

            catalog_results = self.catalog(**query)[:45]

            self.assertEqual([i.id for i in results],
                             [i.id for i in catalog_results])

    @unittest.skip('FIXME: use Collection instead of Topic')
    def test_modifying_query_through_collection(self):

        assgmnt1 = latest_sectionable_nitf.Assignment()

        r1 = self.renderer(context=self.portal,
                           assignment=assgmnt1)

        r1 = r1.__of__(self.portal)

        view = api.content.get_view(u'nitf-filter-list', r1, self.request)

        self.folder.invokeFactory('Topic', id='collection')
        topic = self.folder['collection']
        uid = topic.UID()
        # Choose a different type to show. This key should be ignored
        type_crit = topic.addCriterion('Type', 'ATPortalTypeCriterion')
        type_crit.setValue('Document')
        topic.reindexObject()

        results = view.getResults(limit=45, uid=uid)

        self.assertEqual(len(results), 45)
        query = self.default_query
        query['sort_limit'] = 45

        catalog_results = self.catalog(**query)[:45]

        self.assertEqual([i.id for i in results],
                         [i.id for i in catalog_results])

        # Now, let's add a section, it should also be ignored
        section_crit = topic.addCriterion('section', 'ATSimpleStringCriterion')
        section_crit.setValue('Section 1')
        topic.reindexObject()

        results = view.getResults(limit=45, uid=uid)

        self.assertEqual(len(results), 45)
        query = self.default_query

        catalog_results = self.catalog(**query)[:45]

        self.assertEqual([i.id for i in results],
                         [i.id for i in catalog_results])

        # Now, let's just filter published content, we only get 9 results
        state_crit = topic.addCriterion('review_state',
                                        'ATSimpleStringCriterion')
        state_crit.setValue('published')
        topic.reindexObject()

        results = view.getResults(limit=45, uid=uid)

        self.assertEqual(len(results), 9)
        query = self.default_query
        query['review_state'] = 'published'

        catalog_results = self.catalog(**query)[:45]

        self.assertEqual([i.id for i in results],
                         [i.id for i in catalog_results])

        # Now, let's sort results by section and in reverse
        topic.addCriterion('section', 'ATSortCriterion')
        topic.setSortCriterion('section', True)
        topic.reindexObject()

        results = view.getResults(limit=45, uid=uid)

        self.assertEqual(len(results), 9)
        query = self.default_query
        query['sort_on'] = 'section'

        catalog_results = self.catalog(**query)[:45]

        self.assertEqual([i.id for i in results],
                         [i.id for i in catalog_results])

        # Let's now sort it by section but not in reverse
        topic.setSortCriterion('section', False)
        topic.reindexObject()

        results = view.getResults(limit=45, uid=uid)

        self.assertEqual(len(results), 9)
        query = self.default_query
        del query['sort_order']

        catalog_results = self.catalog(**query)[:45]

        self.assertEqual([i.id for i in results],
                         [i.id for i in catalog_results])

        # Finally, let's just get results filtered for a particular section

        results = view.getResults(section='section 1', limit=45, uid=uid)

        self.assertEqual(len(results), 3)
        query = self.default_query
        query['section'] = 'Section 1'

        catalog_results = self.catalog(**query)[:45]

        self.assertEqual([i.id for i in results],
                         [i.id for i in catalog_results])
