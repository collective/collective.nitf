from five import grok

from zope.interface import Interface
from zope import schema
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName

from Products.CMFPlone.interfaces import IPloneSiteRoot
from plone.directives import form
from plone.formwidget.autocomplete import AutocompleteMultiFieldWidget
from plone.app.registry.browser import controlpanel

from collective.nitf import _
from collective.nitf.config import NORMAL
from collective.nitf.config import PROPERTIES
from collective.nitf.config import URGENCIES

try:
    # only in z3c.form 2.0
    from z3c.form.browser.textlines import TextLinesFieldWidget
except ImportError:
    from plone.z3cform.textlines import TextLinesFieldWidget

from z3c.form.browser.checkbox import CheckBoxFieldWidget

class INITFSettings(form.Schema):
    """ Interface for the form on the control panel. """
    
    form.widget(urgency_list=CheckBoxFieldWidget)
    urgency_list = schema.Choice(
            title=_(u'Priority List (Urgency)'),
            vocabulary=URGENCIES,
            required=False,
            default=NORMAL,
        )

    form.widget(property_list=CheckBoxFieldWidget)
    property_list = schema.Choice(
            title=_(u'Property List'),
            vocabulary=PROPERTIES,
            required=False,
        )


class NITFSettingsEditForm(controlpanel.RegistryEditForm):
    grok.context(IPloneSiteRoot)
    grok.name("nitf_news_settings")
    grok.require("cmf.ManagePortal")

    schema = INITFSettings
    label = _(u"News Article Questions Settings") 
    description = _(u"Here you can modify the settings for News Articles.")

    def updateFields(self):
        super(NITFSettingsEditForm, self).updateFields()

    def updateWidgets(self):
        super(NITFSettingsEditForm, self).updateWidgets()

class NITFSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = NITFSettingsEditForm
