# -*- coding: utf-8 -*-

from zope.i18nmessageid import MessageFactory

from plone.autoform.interfaces import WIDGETS_KEY
from plone.directives.form.schema import TEMP_KEY
from zope import schema as _schema
from plone.app.relationfield.behavior import IRelatedItems

_ = MessageFactory('collective.nitf')


widget = 'collective.z3cform.widgets.multicontent_search_widget.MultiContentSearchFieldWidget'
_directives_values = IRelatedItems.queryTaggedValue(TEMP_KEY)
if _directives_values:
    # groked form
    _directives_values.setdefault(WIDGETS_KEY, {})
    _directives_values[WIDGETS_KEY]['relatedItems'] = widget
else:
    # plone 4.3 not groked form
    _widget_values = IRelatedItems.queryTaggedValue(WIDGETS_KEY, {})
    _widget_values['relatedItems'] = widget
    IRelatedItems.setTaggedValue(WIDGETS_KEY, _widget_values)

_schema.getFields(IRelatedItems)['relatedItems'].index_name = 'Related Items'
