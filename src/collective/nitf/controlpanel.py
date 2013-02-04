# -*- coding: utf-8 -*-
from collective.nitf import _
from collective.nitf import config
from plone.app.registry.browser import controlpanel
from z3c.form import field
from z3c.form import group
from zope import schema
from zope.component import getUtility
from zope.interface import alsoProvides
from plone.registry.interfaces import IRegistry
from plone.directives import form

PORTALTYPES = 'plone.app.vocabularies.ReallyUserFriendlyTypes'


class INITFSettings(form.Schema):
    """ Interface for the control panel form.
    """
    form.widget(available_sections="z3c.form.browser.textlines.TextLinesFieldWidget")
    available_sections = schema.Set(
        title=_(u'Available Sections'),
        description=_(u"List of available sections in the site."),
        required=True,
        default=set(),
        value_type=schema.TextLine(title=_(u'Section')),
    )

    default_section = schema.Choice(
        title=_(u"Default Section"),
        vocabulary=u'collective.nitf.AvailableSections',
        required=False,
    )

    available_genres = schema.List(
        title=_(u"Available Genres"),
        description=_(u"Select the list of available genres in the site. "
                      u"Genres indicate a nature, journalistic or "
                      u"intellectual characteristic of items."),
        required=False,
        default=[],
        value_type=schema.Choice(vocabulary=u'collective.nitf.Genres'),
    )

    default_genre = schema.Choice(
        title=_(u"Default Genre"),
        vocabulary=u'collective.nitf.Genres',
        required=False,
        default=config.DEFAULT_GENRE,
    )

    default_urgency = schema.Choice(
        title=_(u"Default Urgency"),
        vocabulary=u'collective.nitf.Urgencies',
        required=False,
        default=config.DEFAULT_URGENCY,
    )

    relatable_content_types = schema.List(
        title=_(u"Relatable Content Types"),
        description=_(u"Only objects of these content types will be "
                      u"listed in the related items widget."),
        required=False,
        default=config.DEFAULT_RELATABLE_CONTENT_TYPES,
        # we are going to list only the main content types in the widget
        value_type=schema.Choice(vocabulary=PORTALTYPES),
    )


class INITFCharCountSettings(form.Schema):

    show_title_counter = schema.Bool(
        title=_(u'label_show_title_counter',
                default=u"Show a counter for the title?"),
        description=_(u'help_show_title_counter',
                      default=u"If selected, a character counter will show "
                              u"the lenght of the field."),
        required=False,
        default=False,
    )

    title_max_chars = schema.Int(
        title=_(u'label_title_max_chars',
                default=u"Maximum title length"),
        description=_(u'help_title_max_chars',
                      default=u"The limit is just visual; validation is not enforced."),
        default=100,
        required=False,
    )

    title_optimal_chars = schema.Int(
        title=_(u'label_title_optimal_chars',
                default=u"Optimal title length"),
        description=_(u"help_title_optimal_chars",
                      default=u"The optimal length will be between this "
                              u"number and the maximum length of the field."),
        default=100,
        required=False,
    )

    show_description_counter = schema.Bool(
        title=_(u'label_show_description_counter',
                default=u"Show a character counter in the description?"),
        description=_(u'help_show_description_counter',
                      default=u"If selected, a character counter will show "
                              u"the lenght of the field."),
        required=False,
        default=False,
    )

    description_max_chars = schema.Int(
        title=_(u'label_description_max_chars',
                default=u"Maximum description length"),
        description=_(u'help_description_max_chars',
                      default=u"The limit is just visual; validation is not enforced."),
        default=200,
        required=False,
    )

    description_optimal_chars = schema.Int(
        title=_(u'label_description_optimal_chars',
                default=u"Optimal description length"),
        description=_(u"help_description_optimal_chars",
                      default=u"The optimal length will be between this "
                              u"number and the maximum length of the field."),
        default=200,
        required=False,
    )


class NITFGroup(group.Group):
    label = _(u"Default")
    description = _("Default Configuration")
    fields = field.Fields(INITFSettings)


class NITFChartCountGroup(group.Group):
    label = _(u"Character Counter")
    description = _("Character Counter Configuration")
    fields = field.Fields(INITFCharCountSettings)


class INITFSchema(INITFSettings, INITFCharCountSettings):
    """
    """


class NITFSettingsEditForm(controlpanel.RegistryEditForm):
    schema = INITFSchema
    label = _(u"NITF Settings")
    description = _(u"Here you can modify the settings for collective.nitf.")

    fields = INITFSettings
    groups = (NITFChartCountGroup,)

    def getContent(self):
        return AbstractRecordsProxy(self.schema)


class NITFSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = NITFSettingsEditForm


class AbstractRecordsProxy(object):
    """Multiple registry schema proxy.

    This class supports schemas that contain derived fields. The
    settings will be stored with respect to the individual field
    interfaces.
    """

    def __init__(self, schema):
        state = self.__dict__
        state["__registry__"] = getUtility(IRegistry)
        state["__proxies__"] = {}
        state["__schema__"] = schema
        alsoProvides(self, schema)

    def __getattr__(self, name):
        try:
            field = self.__schema__[name]
        except KeyError:
            raise AttributeError(name)
        else:
            proxy = self._get_proxy(field.interface)
            return getattr(proxy, name)

    def __setattr__(self, name, value):
        try:
            field = self.__schema__[name]
        except KeyError:
            self.__dict__[name] = value
        else:
            proxy = self._get_proxy(field.interface)
            return setattr(proxy, name, value)

    def __repr__(self):
        return "<AbstractRecordsProxy for %s>" % self.__schema__.__identifier__

    def _get_proxy(self, interface):
        proxies = self.__proxies__
        return proxies.get(interface) or proxies.setdefault(interface,
                                                            self.__registry__.forInterface(interface))
