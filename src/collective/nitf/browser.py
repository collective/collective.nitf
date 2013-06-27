# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from collective.nitf import _
from collective.nitf.content import INITF
from collective.nitf.controlpanel import INITFCharCountSettings
from collective.nitf.controlpanel import INITFSettings
from collective.nitf.interfaces import INITFLayer
from five import grok
from plone.directives import dexterity
from plone.registry.interfaces import IRegistry
from plone.uuid.interfaces import IUUID
from Products.CMFPlone.utils import getToolByName
from warnings import warn
from zope.component import getUtility
from zope.interface import Interface
from plone.app.imaging.scaling import ImageScaling as BaseImageScaling

import json
import mimetypes


grok.templatedir('templates')


# TODO: enable_form_tabbing must be user selectable
class AddForm(dexterity.AddForm):
    """ Default view looks like a News Item.
    """
    grok.name('collective.nitf.content')
    grok.layer(INITFLayer)
    grok.context(INITF)
    schema = INITF

    def update(self):
        super(AddForm, self).update()
        # iterate over fieldsets
        for group in self.groups:
            # HACK: we need to update criteria of the ObjPathSourceBinder here
            # as we want to list only relatable content types
            if 'relatedItems' in group.widgets.keys():
                registry = getUtility(IRegistry)
                settings = registry.forInterface(INITFSettings)
                widget = group.widgets['relatedItems']
                criteria = widget.source.selectable_filter.criteria
                criteria['portal_type'] = settings.relatable_content_types

    def updateWidgets(self):
        super(AddForm, self).updateWidgets()
        # XXX why we need to do this?
        self.widgets['subtitle'].style = u'width: 100%;'
        self.widgets['IDublinCore.description'].rows = 3
        self.widgets['IDublinCore.description'].style = u'width: 100%;'


class EditForm(dexterity.EditForm):
    """ Default view looks like a News Item.
    """
    grok.context(INITF)
    grok.layer(INITFLayer)
    schema = INITF

    def update(self):
        super(EditForm, self).update()
        # iterate over fieldsets
        for group in self.groups:
            # HACK: we need to update criteria of the ObjPathSourceBinder here
            # as we want to list only relatable content types
            if 'relatedItems' in group.widgets.keys():
                registry = getUtility(IRegistry)
                settings = registry.forInterface(INITFSettings)
                widget = group.widgets['relatedItems']
                criteria = widget.source.selectable_filter.criteria
                criteria['portal_type'] = settings.relatable_content_types

    def updateWidgets(self):
        super(EditForm, self).updateWidgets()
        # XXX why we need to do this?
        self.widgets['subtitle'].style = u'width: 100%;'
        self.widgets['IDublinCore.description'].rows = 3
        self.widgets['IDublinCore.description'].style = u'width: 100%;'


class View(dexterity.DisplayForm):
    """ Default view looks like a News Item.
    """
    grok.context(INITF)
    grok.require('zope2.View')
    grok.layer(INITFLayer)

    def update(self):
        self.context = aq_inner(self.context)

    def _get_brains(self, object_name=None):
        """ Return a list of brains inside the NITF object.
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        path = '/'.join(self.context.getPhysicalPath())
        brains = catalog(Type=object_name, path=path,
                         sort_on='getObjPositionInParent')

        return brains

    def get_images(self):
        """ Return a list of image brains inside the NITF object.
        """
        return self._get_brains('Image')

    def has_images(self):
        """ Return the number of images inside the NITF object.
        """
        return len(self.get_images())

    def get_files(self):
        """ Return a list of file brains inside the NITF object.
        """
        return self._get_brains('File')

    def has_files(self):
        """ Return the number of files inside the NITF object.
        """
        return len(self.get_files())

    def get_links(self):
        """ Return a list of link brains inside the NITF object.
        """
        return self._get_brains('Link')

    def has_links(self):
        """ Return the number of links inside the NITF object.
        """
        return len(self.get_links())

    def get_media(self):
        """ Return a list of object brains inside the NITF object.
        """
        media_ct = [x.title for x in self.context.allowedContentTypes()]
        return self._get_brains(media_ct)

    def has_media(self):
        """ Return the number of media inside the NITF object.
        """
        return len(self.get_media())

    def getText(self):
        warn("Calling getText is deprecated. Use self.text.output instead.",
             DeprecationWarning)
        return self.text.output

    # The purpose of these methods is to emulate those on News Item
    def getImage(self):
        warn("Calling getImage on the view is deprecated. Call it on the object.",
             DeprecationWarning)
        return self.context.getImage()

    def imageCaption(self):
        warn("Calling imageCaption on the view is deprecated. Call it on the object.",
             DeprecationWarning)
        return self.context.imageCaption()

    def tag(self, **kwargs):
        warn("Calling tag on the view is deprecated. Call it on the object.",
             DeprecationWarning)
        return self.context.tag(**kwargs)


# TODO: get rid of this class
class Display_Macros(View):
    grok.context(INITF)
    grok.require('zope2.View')
    grok.layer(INITFLayer)


class Folder_Summary_View(grok.View):
    grok.context(Interface)
    grok.layer(INITFLayer)
    grok.name("folder_summary_view")
    grok.require('zope2.View')


class NITF(View):
    """ Shows news article in NITF XML format.
    """
    grok.context(INITF)
    grok.layer(INITFLayer)
    grok.name('nitf')
    grok.require('zope2.View')

    def update(self):
        self.context = aq_inner(self.context)
        self.uuid = IUUID(self.context)

    def _get_mediatype(self, mimetype):
        """ Return one of the possible values of the media-type controlled
        vocabulary.
        """
        # 'data' and 'other' are also part of the controlled vocabulary; we
        # are not going to use 'data'
        vocabulary = ['text', 'audio', 'image', 'video', 'application']
        for i in vocabulary:
            if mimetype.find(i) != -1:
                return i

        return 'other'

    MEDIA = """
<media media-type="%s">
    <media-reference mime-type="%s" source="%s" alternate-text="%s"%s%s />
    <media-caption>%s</media-caption>
</media>"""

    def get_media(self):
        """ Return a list of object brains inside the NITF object.
        """
        media = []
        # XXX: we could honor original order calling the get_media() method in
        # View; how can we do that?
        results = self.get_images() + self.get_files()
        for r in results:
            obj = r.getObject()
            source = obj.absolute_url()
            (mimetype, encoding) = mimetypes.guess_type(source)
            # if no mime type is detected, result is None; we must change it
            mimetype = mimetype and mimetype or ''
            mediatype = self._get_mediatype(mimetype)
            alternate_text = obj.Title()
            caption = obj.Description()
            # we only include height and/or width if we have a value for them
            height = obj.getHeight()
            height = height and ' height="%s"' % obj.getHeight() or ''
            width = obj.getWidth()
            width = width and ' width="%s"' % obj.getWidth() or ''
            m = self.MEDIA % (mediatype, mimetype, source, alternate_text,
                              height, width, caption)
            media.append(m)

        return media


class NewsML(View):
    """ Shows news article in NewsML XML format.
    """
    grok.context(INITF)
    grok.layer(INITFLayer)
    grok.name('newsml')
    grok.require('zope2.View')

    def version(self):
        """ Returns news article revision number.
        """
        # TODO: get revision number
        return 1

    def nitf_size(self):
        """ Returns size of the news article in NITF format.
        """
        # TODO: calculate size
        return 1000

    ITEM_REF = """
<itemRef href="%s/@@nitf" size="%s"
   contenttype="application/nitf+xml" format="fmt:nitf">
    <title>%s</title>
</itemRef>"""

    def get_related_items(self):
        """ Returns an itemRef tag for each related item (only News Articles).
        """
        items = getattr(self.context, 'relatedItems', None)
        if items is not None:
            related_items = []
            for i in items:
                href = i.to_object.absolute_url()
                size = self.nitf_size()
                title = i.to_object.Title()
                item_ref = self.ITEM_REF % (href, size, title)
                related_items.append(item_ref)
            return related_items


class Media(View):
    grok.context(INITF)
    grok.require('cmf.ModifyPortalContent')


class DeleteMedia(View):
    grok.context(INITF)
    grok.name('delete_media')
    grok.require('cmf.ModifyPortalContent')

    # XXX: This is here, because under certain situations, grok will get the
    # template of 'View' superclass and raise an exception.
    template = None

    def __call__(self):
        delete_id = self.request['id'] if 'id' in self.request else None

        status = {'status': 'error'}
        if delete_id:
            self.context.manage_delObjects([delete_id])
            status['status'] = 'success'

        return json.dumps(status)

    def render(self):
        pass


class CharactersCount(grok.View):
    grok.context(Interface)
    grok.name('characters-count.js')
    grok.require('zope2.View')

    def render(self):

        response = self.request.response
        response.setHeader('content-type', 'text/javascript;;charset=utf-8')
        registry = getUtility(IRegistry)
        settings = registry.forInterface(INITFCharCountSettings)

        count_title = settings.show_title_counter
        count_description = settings.show_description_counter

        counter_text = _(u'Characters left: ')

        config_title = {
            'allowed': settings.title_max_chars,
            'optimal': settings.title_optimal_chars,
            'counterText': counter_text
        }
        config_description = {
            'allowed': settings.description_max_chars,
            'optimal': settings.description_optimal_chars,
            'counterText': counter_text
        }

        title = ''
        description = ''

        if count_title:
            title = '$("#form-widgets-IDublinCore-title").charCount(%s);' % json.dumps(config_title)

        if count_description:
            description = '$("#form-widgets-IDublinCore-description").charCount(%s);' % json.dumps(config_description)

        script = '$(document).ready(function() {%s %s});' % (title, description)
        return script


class Nitf_Galleria(View):
    grok.context(INITF)
    grok.layer(INITFLayer)
    grok.require('zope2.View')
    grok.name('nitf_galleria')

    def imagesJson(self):
        """ """
        try:
            img_brains = self.get_images()
        except IndexError:
            img_brains = None
        if img_brains:
            data = [{'image': str(brain.getPath() + '/image_preview'),
                     'title': brain.Title,
                     'description': brain.Description, 'right': brain.Rights(),
                     'link': brain.getURL()} for brain in img_brains]
        else:
            data = []

        return json.dumps(data)


class ImageScaling(BaseImageScaling):
    """ view used for generating (and storing) image scales """

    def __init__(self, context, request):
        self.image = context.getImage()
        self.context = self.image or context
        self.request = request

    def scale(self, fieldname=None, scale=None, height=None, width=None,
              **parameters):
        if not self.image:
            return None
        view = self.image.restrictedTraverse('@@images')
        return view.scale(fieldname, scale, height, width, **parameters)
