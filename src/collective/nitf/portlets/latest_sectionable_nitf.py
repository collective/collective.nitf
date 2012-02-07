# -*- coding: utf-8 -*-

from five import grok

from zope.interface import implements
from zope.component import getMultiAdapter, getUtility

from Products.CMFCore.utils import getToolByName

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

from zope import schema
from zope.formlib import form

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from zope.schema.interfaces import IVocabularyFactory

from collective.prettydate.interfaces import IPrettyDate
from zope.interface import Interface

from zope.schema.vocabulary import SimpleVocabulary

from collective.nitf import _


class NitfFilterList(grok.View):
    grok.context(Interface)
    grok.name("nitf-filter-list")
    grok.require("zope2.View")

    template = ViewPageTemplateFile('nitf_filter_list.pt')

    def __call__(self):
        section = self.request.get('section', None)
        if section:
            result = self.render(section)
        else:
            result = self.render()

        return result

    def render(self, section=None, limit=10, pretty_date=True):
        pc = getToolByName(self.context, 'portal_catalog')
        query = {'portal_type': 'collective.nitf.content',
                 'sort_on': 'created',
                 'sort_order': 'reverse',
                 'sort_limit': limit}

        if section and section != 'all':
            vocab = getUtility(IVocabularyFactory,
                           name=u'collective.nitf.Sections')(self.context)

            query.update({'section': vocab.getTermByToken(section).value})

        results = pc(**query)[:limit]

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

    def __init__(self,
                 header=u"",
                 limit=10,
                 pretty_date=True):

        self.header = header
        self.limit = limit
        self.pretty_date = pretty_date

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

        results = view.render(section,
                              self.data.limit,
                              self.data.pretty_date)

        return results

    def getAvailableSections(self):
        vocab = getUtility(IVocabularyFactory,
                           name=u'collective.nitf.Sections')(self.context)

        values = SimpleVocabulary([SimpleVocabulary.createTerm(_(u"All"),
                                                               "all",
                                                               _(u"All"))] +
                                   vocab._terms)

        return values


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
