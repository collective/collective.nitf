# -*- coding: utf-8 -*-
from five import grok

from zope import schema
from zope.interface import Interface
from zope.schema.vocabulary import SimpleVocabulary

from z3c.form.browser.textlines import TextLinesFieldWidget

from plone.app.registry.browser import controlpanel
from plone.registry.interfaces import IRegistry

from zope.component import getUtility
from zope.app.form.browser import RadioWidget, MultiSelectWidget
from zope.schema.interfaces import IContextSourceBinder

from collective.nitf import _
from collective.nitf import config


class INITFSettings(Interface):
    """Interface for the form on the control panel.
    """

    sections = schema.Set(
            title=_(u'Available Sections'),
            required=True,
            default=set(),
            value_type=schema.TextLine(title=_(u'Section')),)

    default_section = schema.Choice(
            title=_(u'Default Section'),
            vocabulary=u'collective.nitf.Sections',
            required=False,)

    default_genre = schema.Choice(
            title=_(u'Default Genre'),
            vocabulary=config.GENRES,
            required=False,
            default=config.DEFAULT_GENRE,)

    possible_genres = schema.List(title=_(u'possible genres'),
            description=_(u"Choose genres to use in the site"),
                            required=False,
                             value_type = schema.Choice(vocabulary=config.GENRES,),
                             )

    default_urgency = schema.Choice(
            title=_(u'Default Urgency'),
            vocabulary=config.URGENCIES,
            required=False,
            default=config.DEFAULT_URGENCY,)


class NITFSettingsEditForm(controlpanel.RegistryEditForm):
    """
    """

    schema = INITFSettings
    label = _(u'NITF Settings')
    description = _(u'Here you can modify the settings for collective.nitf.')

    def updateFields(self):
        super(NITFSettingsEditForm, self).updateFields()
        self.fields['sections'].widgetFactory = TextLinesFieldWidget

    def updateWidgets(self):
        super(NITFSettingsEditForm, self).updateWidgets()
        self.widgets['sections'].rows = 8
        self.widgets['sections'].style = u'width: 30%;'
        #import pdb; pdb.set_trace()


class NITFSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = NITFSettingsEditForm

@grok.provider(IContextSourceBinder)
def availableGenres(context):
    registry = getUtility(IRegistry)
    terms = []
    if registry is not None:
        settings = registry.forInterface(INITFSettings)
        if settings.possible_genres:
            for genre in settings.possible_genres:
                terms.append(SimpleVocabulary.createTerm(genre,
                    genre.encode('utf-8'), genre))

    if not terms:
        return config.GENRES
    return SimpleVocabulary(terms)
