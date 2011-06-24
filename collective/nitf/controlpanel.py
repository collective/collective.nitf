from five import grok

from zope.interface import Interface
from zope import schema
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName

from Products.CMFPlone.interfaces import IPloneSiteRoot
from plone.app.registry.browser import controlpanel

from collective.nitf import _

try:
    # only in z3c.form 2.0
    from z3c.form.browser.textlines import TextLinesFieldWidget
except ImportError:
    from plone.z3cform.textlines import TextLinesFieldWidget

from z3c.form.browser.checkbox import CheckBoxFieldWidget

class INITFSettings(Interface):
    """ Interface for the form on the control panel. """

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
