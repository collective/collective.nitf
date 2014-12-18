# -*- coding: utf-8 -*-

from collective.nitf.content import INITF
from collective.nitf.testing import INTEGRATION_TESTING
from plone.app.referenceablebehavior.referenceable import IReferenceable
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.fti import DexterityFTI
from plone.dexterity.interfaces import IDexterityFTI
from plone.uuid.interfaces import IAttributeUUID
from StringIO import StringIO
from zope.component import createObject
from zope.component import queryUtility

import unittest2 as unittest

zptlogo = (
    'GIF89a\x10\x00\x10\x00\xd5\x00\x00\xff\xff\xff\xff\xff\xfe\xfc\xfd\xfd'
    '\xfa\xfb\xfc\xf7\xf9\xfa\xf5\xf8\xf9\xf3\xf6\xf8\xf2\xf5\xf7\xf0\xf4\xf6'
    '\xeb\xf1\xf3\xe5\xed\xef\xde\xe8\xeb\xdc\xe6\xea\xd9\xe4\xe8\xd7\xe2\xe6'
    '\xd2\xdf\xe3\xd0\xdd\xe3\xcd\xdc\xe1\xcb\xda\xdf\xc9\xd9\xdf\xc8\xd8\xdd'
    '\xc6\xd7\xdc\xc4\xd6\xdc\xc3\xd4\xda\xc2\xd3\xd9\xc1\xd3\xd9\xc0\xd2\xd9'
    '\xbd\xd1\xd8\xbd\xd0\xd7\xbc\xcf\xd7\xbb\xcf\xd6\xbb\xce\xd5\xb9\xcd\xd4'
    '\xb6\xcc\xd4\xb6\xcb\xd3\xb5\xcb\xd2\xb4\xca\xd1\xb2\xc8\xd0\xb1\xc7\xd0'
    '\xb0\xc7\xcf\xaf\xc6\xce\xae\xc4\xce\xad\xc4\xcd\xab\xc3\xcc\xa9\xc2\xcb'
    '\xa8\xc1\xca\xa6\xc0\xc9\xa4\xbe\xc8\xa2\xbd\xc7\xa0\xbb\xc5\x9e\xba\xc4'
    '\x9b\xbf\xcc\x98\xb6\xc1\x8d\xae\xbaFgs\x00\x00\x00\x00\x00\x00\x00\x00'
    '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    '\x00,\x00\x00\x00\x00\x10\x00\x10\x00\x00\x06z@\x80pH,\x12k\xc8$\xd2f\x04'
    '\xd4\x84\x01\x01\xe1\xf0d\x16\x9f\x80A\x01\x91\xc0ZmL\xb0\xcd\x00V\xd4'
    '\xc4a\x87z\xed\xb0-\x1a\xb3\xb8\x95\xbdf8\x1e\x11\xca,MoC$\x15\x18{'
    '\x006}m\x13\x16\x1a\x1f\x83\x85}6\x17\x1b $\x83\x00\x86\x19\x1d!%)\x8c'
    '\x866#\'+.\x8ca`\x1c`(,/1\x94B5\x19\x1e"&*-024\xacNq\xba\xbb\xb8h\xbeb'
    '\x00A\x00;')


class ContentTypeTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

        self.folder.invokeFactory('collective.nitf.content', 'n1')
        self.n1 = self.folder['n1']

    def test_adding(self):
        self.assertTrue(INITF.providedBy(self.n1))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='collective.nitf.content')
        self.assertIsNotNone(fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='collective.nitf.content')
        schema = fti.lookupSchema()
        self.assertEqual(INITF, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='collective.nitf.content')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(INITF.providedBy(new_object))

    def test_is_referenceable(self):
        self.assertTrue(IReferenceable.providedBy(self.n1))
        self.assertTrue(IAttributeUUID.providedBy(self.n1))

    def test_locking_behavior_available(self):
        from plone.app.lockingbehavior.behaviors import ILocking
        self.assertTrue(ILocking.providedBy(self.n1))

    def test_action_is_registered(self):
        fti = queryUtility(IDexterityFTI, name='collective.nitf.content')
        actions = [a.id for a in fti.listActions()]
        self.assertIn('media', actions)

    def test_is_empty(self):
        # the new article has no content inside
        self.assertTrue(self.n1.is_empty())

        # Image doesn't count, so it should be still empty
        self.n1.invokeFactory('Image', 'foo')
        self.assertTrue(self.n1.is_empty())

        # File and Link count
        self.n1.invokeFactory('File', 'bar')
        self.assertFalse(self.n1.is_empty())
        self.n1.manage_delObjects('bar')

        self.n1.invokeFactory('Link', 'baz')
        self.assertFalse(self.n1.is_empty())

    def test_image_scale(self):
        self.assertIsNone(self.n1.getImage())

        self.n1.invokeFactory('Image', 'foo', title='bar', description='baz',
                              image=StringIO(zptlogo))
        view = self.n1.restrictedTraverse('@@images')
        scale = view.scale('image', 'thumb')
        self.assertEqual(scale.height, 16)
        self.assertEqual(scale.width, 16)

    def test_getImage(self):
        self.assertIsNone(self.n1.getImage())

        self.n1.invokeFactory('Image', 'foo', title='bar', description='baz',
                              image=StringIO(zptlogo))
        image = self.n1.getImage()
        self.assertEqual(image.id, 'foo')
        self.assertEqual(image.Title(), 'bar')
        self.assertEqual(image.Description(), 'baz')

    def test_imageCaption(self):
        imageCaption = self.n1.imageCaption
        self.assertIsNone(imageCaption())
        self.n1.invokeFactory('Image', 'foo', title='bar', description='baz',
                              image=StringIO(zptlogo))
        self.assertEqual(imageCaption(), 'baz')

    def test_image_thumb(self):
        thumb = self.n1.image_thumb

        # no images in news article, so no thumb must be present
        self.assertIsNone(thumb())

        self.n1.invokeFactory('Image', 'foo', title='bar', description='baz',
                              image=StringIO(zptlogo))
        self.assertIsNotNone(thumb())

    def test_tag(self):
        tag = self.n1.tag

        # no images in news article, so no tag must be present
        self.assertIsNone(tag())

        self.n1.invokeFactory('Image', 'foo', title='bar', description='baz',
                              image=StringIO(zptlogo))

        # image title must be in both, alt and title attributes
        self.assertIn('alt="baz" title="bar"', tag())

        # image size
        self.assertIn('height="16" width="16', tag())

        # image scale using @@images
        self.assertIn('src="http://nohost/plone/test-folder/n1/foo/@@images/',
                      tag(scale='preview'))

        # image class
        self.assertIn('class="myClass"', tag(css_class='myClass'))


IMAGE_SCHEMA = '''<model xmlns="http://namespaces.plone.org/supermodel/schema"
       xmlns:marshal="http://namespaces.plone.org/supermodel/marshal"
       xmlns:i18n="http://xml.zope.org/namespaces/i18n"
       i18n:domain="plone">
  <schema>
    <field name="title" type="zope.schema.TextLine">
      <description />
      <required>False</required>
      <title>Title</title>
    </field>
    <field name="description" type="zope.schema.Text">
      <description />
      <required>False</required>
      <title>Description</title>
    </field>
    <field name="image" type="plone.namedfile.field.NamedBlobImage"
        marshal:primary="true">
      <description />
      <title i18n:translate="Image">Image</title>
    </field>
  </schema>
</model>'''


def dummy_image(data):
    from plone.namedfile.file import NamedBlobImage
    return NamedBlobImage(
        data=data,
        filename=u'zptlogo.gif')


class DexterityImageTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUpImageType(self):
        portal = self.portal
        tt = portal.portal_types
        del tt['Image']
        fti = DexterityFTI('Image')
        portal.portal_types._setObject('Image', fti)
        fti.model_source = IMAGE_SCHEMA

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.setUpImageType()
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

        self.folder.invokeFactory('collective.nitf.content', 'n1')
        self.n1 = self.folder['n1']

    def test_image_scale(self):
        self.assertIsNone(self.n1.getImage())

        self.n1.invokeFactory('Image', 'foo', title='bar', description='baz',
                              image=dummy_image(zptlogo))
        view = self.n1.restrictedTraverse('@@images')
        scale = view.scale('image', 'thumb')
        self.assertEqual(scale.height, 16)
        self.assertEqual(scale.width, 16)

    def test_getImage(self):
        self.assertIsNone(self.n1.getImage())

        self.n1.invokeFactory('Image', 'foo', title='bar', description='baz',
                              image=dummy_image(zptlogo))
        image = self.n1.getImage()
        self.assertEqual(image.id, 'foo')
        self.assertEqual(image.Title(), 'bar')
        self.assertEqual(image.Description(), 'baz')

    def test_imageCaption(self):
        imageCaption = self.n1.imageCaption
        self.assertIsNone(imageCaption())
        self.n1.invokeFactory('Image', 'foo', title='bar', description='baz',
                              image=dummy_image(zptlogo))
        self.assertEqual(imageCaption(), 'baz')

    def test_image_thumb(self):
        thumb = self.n1.image_thumb

        # no images in news article, so no thumb must be present
        self.assertIsNone(thumb())

        self.n1.invokeFactory('Image', 'foo', title='bar', description='baz',
                              image=dummy_image(zptlogo))
        self.assertIsNotNone(thumb())

    def test_tag(self):
        tag = self.n1.tag

        # no images in news article, so no tag must be present
        self.assertIsNone(tag())

        self.n1.invokeFactory('Image', 'foo', title='bar', description='baz',
                              image=dummy_image(zptlogo))

        # image title must be in both, alt and title attributes
        self.assertIn('alt="baz" title="bar"', tag())

        # image size
        self.assertIn('height="16" width="16', tag())

        # image scale using @@images
        self.assertIn('src="http://nohost/plone/test-folder/n1/foo/@@images/',
                      tag(scale='preview'))

        # image class
        self.assertIn('class="myClass"', tag(css_class='myClass'))
