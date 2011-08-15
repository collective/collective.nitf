# -*- coding: utf-8 -*-

import math
import unicodedata

from Acquisition import aq_inner

from five import grok
from zope import schema
from zope.component import getUtility
from zope.component import getMultiAdapter
from zope.interface import Interface
from zope.interface import alsoProvides
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary

from Products.ATContentTypes.interfaces import IImageContent
from Products.ATContentTypes.interfaces import IATLink
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.utils import getToolByName

from plone.app.layout.viewlets.interfaces import IAboveContentBody
from plone.app.layout.viewlets.interfaces import IHtmlHeadLinks
from plone.app.textfield import RichText
from plone.app.textfield.interfaces import ITransformer
from plone.directives import form
from plone.directives import dexterity
from plone.indexer import indexer
from plone.registry.interfaces import IRegistry

from collective.nitf import _
from collective.nitf import config
from collective.nitf import INITFBrowserLayer
from collective.nitf.controlpanel import INITFSettings

VIDEO_MIMETYPES = ['video/mp4', 'video/x-flv']
IMAGE_MIMETYPES = ['image/jpeg', 'image/gif', 'image/png']


class INITF(form.Schema):
    """A news item based on the News Industry Text Format specification.
    """

    #title = schema.TextLine()
        # nitf/head/title and nitf/body/body.head/hedline/hl1

    form.order_after(subtitle='IDublinCore.title')
    subtitle = schema.TextLine(
            # nitf/body/body.head/hedline/hl2
            title=_(u'Subtitle'),
            description=_(u'help_subtitle',
                          default=u'A subordinate headline for the article.'),
            required=False,
            default=u'',
        )

    #abstract = schema.TextLine()
        # nitf/body/body.head/abstract

    byline = schema.TextLine(
            # nitf/body/body.head/byline/person
            title=_(u'Author'),
            required=False,
            default=u'',
        )

    text = RichText(
            # nitf/body/body.content
            title=_(u'Body text'),
            required=False,
        )

    kind = schema.Choice(
            # nitf/head/tobject/tobject.property/@tobject.property.type
            title=_(u'News Type'),
            vocabulary=config.NEWS_TYPES,
        )

    section = schema.Choice(
            # nitf/head/pubdata/@position.section
            title=_(u'Section'),
            description=_(u'help_section',
                          default=u'Named section where the article will '
                                   'appear.'),
            vocabulary=u'collective.nitf.Sections',
        )

    urgency = schema.Choice(
            # nitf/head/docdata/urgency/@ed-urg
            title=_(u'Urgency'),
            description=_(u'help_urgency',
                          default=u'News importance.'),
            vocabulary=config.URGENCIES,
        )

    form.order_after(location='IRelatedItems.relatedItems')
    location = schema.TextLine(
            # nitf/head/docdata/evloc
            title=_(u'Location'),
            description=_(u'help_location',
                          default=u'Event location. Where an event took '
                                   'place (as opposed to where the story was '
                                   'written).'),
            required=False,
        )


@form.default_value(field=INITF['kind'])
def kind_default_value(data):
    registry = getUtility(IRegistry)
    settings = registry.forInterface(INITFSettings)
    return settings.default_kind


class ImageContentAdapter(SchemaAdapterBase, grok.Adapter):
    grok.context(INITF)
    grok.provides(IImageContent)

    def __init__(self, context):
        super(ImageContentAdapter, self).__init__(context)
        self.context = context

    def getImage(self):
        img = None
        if len(self.context.objectIds()):
            return self.context[self.context.objectIds()[0]]
        return

    def setImage(self):
        return

    def tag(self):
        return

alsoProvides(INITF, IImageContent)


class SectionsVocabulary(object):
    """Creates a vocabulary with the sections stored in the registry; the
    vocabulary is normalized to allow the use of non-ascii characters.
    """
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(INITFSettings)
        items = []
        for section in settings.sections:
            token = unicodedata.normalize('NFKD', section).encode('ascii', 'ignore').lower()
            items.append(SimpleVocabulary.createTerm(section, token, section))
        return SimpleVocabulary(items)

grok.global_utility(SectionsVocabulary, name=u'collective.nitf.Sections')


@form.default_value(field=INITF['section'])
def section_default_value(data):
    registry = getUtility(IRegistry)
    settings = registry.forInterface(INITFSettings)
    return settings.default_section


@form.default_value(field=INITF['urgency'])
def urgency_default_value(data):
    registry = getUtility(IRegistry)
    settings = registry.forInterface(INITFSettings)
    return settings.default_urgency


@indexer(INITF)
def textIndexer(obj):
    """SearchableText contains id, title, subtitle, abstract, author and body
    text as plain text.
    """
    transformer = ITransformer(obj)
    text = transformer(obj.text, 'text/plain')
    return '%s %s %s %s %s %s %s' % (obj.id,
                                     obj.Title(),
                                     obj.subtitle,
                                     obj.Description(),
                                     obj.byline,
                                     text,
                                     obj.location)
grok.global_adapter(textIndexer, name='SearchableText')


class IMediaView(Interface):
    """Marker interface for media views.
    """


class Media_View(dexterity.DisplayForm):
    grok.context(INITF)
    grok.name('media_view')
    grok.title(u'Media View')
    grok.require('zope2.View')
    grok.layer(INITFBrowserLayer)

    def update(self):
        self.catalog = getToolByName(self.context, 'portal_catalog')
        self.get_images()

    def get_images(self):
        return self.get_media_files(types=('Image',))

    def get_videos(self):
        return self.get_media_files(types=('File',))

    def get_media_files(self, types=('Image', 'File',), limit=None):
        context_path = '/'.join(self.context.getPhysicalPath())
        media_brains = self.catalog.searchResults(
                        {'Type': types,
                         'path': {'query': context_path,
                                  'depth': 1},
                         },
                        sort_on="getObjPositionInParent",
                        limit=limit)
        media_items = []
        for brain in media_brains:
            ibrain = {'id': brain.id,
                      'title': brain.Title,
                      'description': brain.Description,
                      'image_url': brain.getURL(),
                      }
            if brain.getObject().getContentType() in IMAGE_MIMETYPES:
                ibrain['media_type'] = 'image'
            elif brain.getObject().getContentType() in VIDEO_MIMETYPES:
                ibrain['media_type'] = 'video'
            else:
                ibrain['media_type'] = None
            media_items.append(ibrain)
        return media_items


class NewsItem_View(Media_View):
    grok.context(INITF)
    grok.name('newsitem_view')
    grok.require('zope2.View')
    grok.layer(INITFBrowserLayer)

    def image(self):
        imgs = self.get_media_files(types=('Image',), limit=1)
        if len(imgs):
            return imgs[0]


class NewsMedia_View(NewsItem_View):
    grok.context(INITF)
    grok.layer(INITFBrowserLayer)
    grok.name('newsmedia_view')
    grok.require('zope2.View')
    grok.template('newsmedia_view')
    grok.view(IMediaView)


class MediaViewletManager(grok.ViewletManager):
    grok.context(INITF)
    grok.name('collective.nitf.carousel')
    grok.view(Media_View)
    grok.layer(INITFBrowserLayer)


class MediaViewlet(grok.Viewlet):
    grok.context(INITF)
    grok.name('collective.nitf.media.tile')
    grok.viewletmanager(IAboveContentBody)
    grok.view(NewsMedia_View)
    grok.template('media_viewlet')
    grok.require('zope2.View')
    grok.layer(INITFBrowserLayer)

    image_size = 'tile'

    def update(self, image_size=None):
        if image_size is not None:
            self.image_size = image_size
        self.media_name = "media-%s" % self.image_size

    def mediaRows(self, keys, cols='5'):
        rows = []
        if not cols or not keys:
            return rows
        rows_number = int(math.ceil(float(len(keys)) / float(cols)))
        for row in range(rows_number):
            this_row = []
            start = row * int(cols)
            end = start + int(cols)
            for key in keys[start:end]:
                this_row.append(key)
            rows.append(this_row)
        return rows


class MediaPreviewViewlet(MediaViewlet):
    grok.context(INITF)
    grok.name('collective.nitf.media.preview')
    grok.viewletmanager(MediaViewletManager)
    grok.view(Media_View)
    grok.layer(INITFBrowserLayer)

    image_size = 'preview'


class MediaLinksViewlet(grok.Viewlet):
    grok.context(INITF)
    grok.name('collective.nitf.links.media')
    grok.template('media_links')
    grok.viewletmanager(IHtmlHeadLinks)
    grok.layer(INITFBrowserLayer)


class Embed(dexterity.DisplayForm):
    grok.context(INITF)
    grok.require('zope2.View')

    def links(self):
        """Return a catalog search result of links to show.
        """

        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')

        links = catalog(object_provides=IATLink.__identifier__,
                        path='/'.join(context.getPhysicalPath()),
                        sort_on='getObjPositionInParent')

        links = [brain.getObject() for brain in links]
        links = [{'title': obj.Title(),
                  'url': obj.remoteUrl,
                  'description': obj.Description()} for obj in links]
        return links

    def key(self):
        """Return Embedly key.
        """
        registry = getUtility(IRegistry)
        settings = registry.forInterface(INITFSettings)
        return settings.embedly_key


class Media_Sorter(dexterity.DisplayForm):
    grok.context(INITF)
    grok.require('cmf.ModifyPortalContent')


class Media_Uploader(dexterity.DisplayForm):
    grok.context(INITF)
    grok.require('cmf.ModifyPortalContent')

    files = []

    def update(self, uploaderfiles=None):
        #self.files = self.request.form.items()
        #if uploaderfiles is not None:
        #    self.files = uploaderfiles
        if getattr(self.request, "METHOD", None):
            if self.request["METHOD"] == "POST":
                self.files = u"Post"
                return u"POST"
