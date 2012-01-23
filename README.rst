***************
collective.nitf
***************

.. contents:: Table of Contents

Overview
--------

A content type inspired on the News Industry Text Format specification.

Requirements
------------

* Plone >= 4.1.x (http://plone.org/products/plone)
* Dexterity >= 1.1 (http://pypi.python.org/pypi/plone.app.dexterity)

Introduction
------------

News articles in Plone are instances of the 'News Item' content type: they can
contain a title, a description, a body text, an image and some basic metadata.
If you publish a couple of items from time to time, this is fine.

But suppose you have to publish dozens of items everyday... How do you tell
your readers who they are about? What do they cover? Where do they took place?
And, more important, how do you classify them? How do you organize them? How
do you tell your readers which ones are newsworthy?

To solve these, and other issues, the `IPTC <http://www.iptc.org/>`_ developed
XML standards to define the content and structure of news articles. `NITF
<http://www.nitf.org/>`_, `NewsML <http://www.newsml.org/>`_ and `NewsCodes
<http://www.iptc.org/NewsCodes/>`_ are among these standards and they support
the classification, identification and description of a huge number of news
articles characteristics.

NITF is intended to structure independent news articles and this package aims
to implement a content type inspired by the specification.

Helper views
^^^^^^^^^^^^

All news articles provide a @@nitf view that is available although is not
registered.

In the near future we are going to implement a @@newsml view also.

Validating
^^^^^^^^^^

You can validate the output of the @@nitf view using services like `XML
validation <http://www.xmlvalidation.com/>`_.

You may use the NITF `Document Type Definition
<http://www.iptc.org/std/NITF/3.5/specification/nitf-3-5.dtd>`_ version 3.5
and the `XHTML Ruby Module
<http://www.iptc.org/std/NITF/3.5/specification/xhtml-ruby-1.mod>`_ associated
with it.
