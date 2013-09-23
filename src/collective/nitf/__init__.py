# -*- coding: utf-8 -*-

from zope.i18nmessageid import MessageFactory

from plone.app.dexterity.behaviors.metadata import ICategorization
from plone.autoform.interfaces import WIDGETS_KEY
from plone.directives.form.schema import TEMP_KEY
from zope import schema as _schema

_ = MessageFactory('collective.nitf')


widget = 'collective.z3cform.widgets.multicontent_search_widget.MultiContentSearchFieldWidget'
_directives_values = ICategorization.queryTaggedValue(TEMP_KEY)
if _directives_values:
    # groked form
    _directives_values.setdefault(WIDGETS_KEY, {})
    _directives_values[WIDGETS_KEY]['relatedItem'] = widget
else:
    # plone 4.3 not groked form
    _widget_values = ICategorization.queryTaggedValue(WIDGETS_KEY, {})
    _widget_values['relatedItem'] = widget
    ICategorization.setTaggedValue(WIDGETS_KEY, _widget_values)

_schema.getFields(ICategorization)['relatedItem'].index_name = 'Related Items'
