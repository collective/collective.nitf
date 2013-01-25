# -*- coding: utf-8 -*-

from AccessControl.unauthorized import Unauthorized
from collective.nitf import _
from collective.prettydate.interfaces import IPrettyDate
from five import grok
from plone.app.portlets.portlets import base
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.portlets.interfaces import IPortletDataProvider
from Products.CMFCore.utils import getToolByName
from zope import schema
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter, getUtility
from zope.formlib import form
from zope.interface import implements
from zope.interface import Interface
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary


class NitfFilterList(grok.View):
    grok.context(Interface)
    grok.name("nitf-filter-list")
    grok.require("zope2.View")

    template = ViewPageTemplateFile('nitf_filter_list.pt')

    def __call__(self):
        section = self.request.get('nitf-section-filter', None)
        collection_uid = self.request.get('nitf-filter-collection-uuid', None)
        if not section:
            section = None
        if not collection_uid:
            collection_uid = None

        result = self.render(section=section, uid=collection_uid)

        return result

    def getResults(self, section=None, limit=10, uid=None):
        uc = getToolByName(self.context, 'uid_catalog')
        pc = getToolByName(self.context, 'portal_catalog')

        collection = None
        query = {}
        if uid:
            try:
                collection = uc(UID=uid)[0].getObject()
                query = collection.buildQuery()
            except IndexError:
                pass

        # Let's force the portal_type to be collective.nitf.content
        query['Type'] = ('News Article',)

        # Now, let's try and load default values if not defined in the
        # collection
        if 'sort_on' not in query:
            query['sort_on'] = 'created'

            if 'sort_order' not in query:
                query['sort_order'] = 'reverse'

        if 'sort_limit' not in query:
            query['sort_limit'] = limit

        # Now, let's remove any trace of a section (this should be filtered
        # from portlet selection)
        if 'section' in query:
            del query['section']

        if section and section != 'all':
            util = getUtility(IVocabularyFactory,
                              name=u'collective.nitf.AvailableSections')
            vocab = util(self.context)

            query.update({'section': vocab.getTermByToken(section).value})

        results = pc(**query)[:limit]

        return results

    def render(self, pretty_date=True, **kw):
        results = self.getResults(**kw)
        return self.template(results=results, pretty_date=pretty_date)

    def getPrettyDate(self, date):
        # Returns human readable date for the tweet
        date_utility = getUtility(IPrettyDate)
        date = date_utility.date(date)

        return date


class ILatestSectionableNITFPortlet(IPortletDataProvider):
    """
    A portlet which shows the latest NITF created and can be filtered
    by section.
    """

    header = schema.TextLine(
        title=_(u'Header'),
        description=_(u"The header for the portlet. Leave empty for none."),
        required=False)

    limit = schema.Int(
        title=_(u"Limit"),
        description=_(u"Specify the maximum number of items to show in the "
                      u"portlet. Leave this blank to show all items."),
        default=10,
        required=False)

    pretty_date = schema.Bool(
        title=_(u'Pretty dates'),
        description=_(u"Show dates in a pretty format (ie. '4 hours ago')."),
        default=True,
        required=False)

    filter_collection = schema.Choice(
        title=_(u"Filter collection"),
        description=_(u"Use the criteria from this collection to modify the "
                      u"search results and order."),
        required=False,
        source=SearchableTextSourceBinder(
            {'portal_type': ('Topic', 'Collection')},
            default_query='path:'))


class Assignment(base.Assignment):
    """
    Portlet assignment.
    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(ILatestSectionableNITFPortlet)

    header = u""
    limit = 10
    pretty_date = True
    filter_collection = None

    def __init__(self,
                 header=u"",
                 limit=10,
                 pretty_date=True,
                 filter_collection=None):

        self.header = header
        self.limit = limit
        self.pretty_date = pretty_date
        self.filter_collection = filter_collection

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen. Here, we use the title that the user gave.
        """
        return _(u"Latest Sectionable NITF")


class Renderer(base.Renderer):

    render = ViewPageTemplateFile('latest_sectionable_nitf.pt')

    def getHeader(self):
        """
        Returns the header for the portlet
        """
        return self.data.header

    def getResults(self, section=None):
        view = getMultiAdapter((self.context, self.request),
                               name="nitf-filter-list")

        uid = None
        if self.data.filter_collection:
            uid = self.getCollectionUID()

        results = view.render(section=section,
                              limit=self.data.limit,
                              pretty_date=self.data.pretty_date,
                              uid=uid)

        return results

    def getAvailableSections(self):
        vocab = getUtility(IVocabularyFactory,
                           name=u'collective.nitf.AvailableSections')(self.context)

        values = SimpleVocabulary([SimpleVocabulary.createTerm(_(u"All"),
                                                               "all",
                                                               _(u"All"))] +
                                  vocab._terms)

        return values

    def getCollectionUID(self):
        portal = self.context.portal_url.getPortalObject()
        context = portal

        for i in self.data.filter_collection.split('/')[1:]:
            try:
                context = context.restrictedTraverse(i)
            except Unauthorized:
                return ''

        if context is not portal and context.portal_type in ('Topic', 'Collection'):
            return context.UID()
        else:
            return ''


class AddForm(base.AddForm):

    form_fields = form.Fields(ILatestSectionableNITFPortlet)

    label = _(u"Add latest NITF Portlet")
    description = _(u"This portlet display a list of latest NITF created. "
                    u"It allows to filter NITF from different sections.")

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):

    form_fields = form.Fields(ILatestSectionableNITFPortlet)

    label = _(u"Add latest NITF Portlet")
    description = _(u"This portlet display a list of latest NITF created. "
                    u"It allows to filter NITF from different sections.")
