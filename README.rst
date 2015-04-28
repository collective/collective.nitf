===============
collective.nitf
===============

.. contents:: Table of Contents

Life, the Universe, and Everything
----------------------------------

News articles in Plone are instances of the 'News Item' content type: they can
contain a title, a description, a body text, an image and some basic metadata.
If you publish a couple of items from time to time, this is fine.

But suppose you have to publish dozens of items everyday... How do you tell
your readers who they are about? What do they cover? Where do they took place?
And, more important, how do you classify them? How do you organize them? How
do you tell your readers which ones are newsworthy?

To solve these, and other issues, the `IPTC`_ developed XML standards to
define the content and structure of news articles. `NITF`_, `NewsML`_ and
`NewsCodes`_ are among these standards and they support the classification,
identification and description of a huge number of news articles
characteristics.

NITF is intended to structure independent news articles and this package aims
to implement a content type inspired by the specification.

Mostly Harmless
---------------

.. image:: https://secure.travis-ci.org/collective/collective.nitf.png?branch=1.x
    :alt: Travis CI badge
    :target: http://travis-ci.org/collective/collective.nitf

.. image:: https://coveralls.io/repos/collective/collective.nitf/badge.png?branch=1.x
    :alt: Coveralls badge
    :target: https://coveralls.io/r/collective/collective.nitf

.. image:: https://pypip.in/d/collective.nitf/badge.png
    :alt: Downloads
    :target: https://pypi.python.org/pypi/collective.nitf/

Got an idea? Found a bug? Let us know by `opening a support ticket`_.

Don't Panic
-----------

Installation
^^^^^^^^^^^^

To enable this product in a buildout-based installation:

1. Edit your buildout.cfg and add ``collective.nitf`` to the list of eggs to
   install::

    [buildout]
    ...
    eggs =
        collective.nitf

After updating the configuration you need to run ''bin/buildout'', which will
take care of updating your system.

Go to the 'Site Setup' page in a Plone site and click on the 'Add-ons' link.

Check the box next to ``collective.nitf`` and click the 'Activate' button.

.. Note:

	You may have to empty your browser cache and save your resource registries
	in order to see the effects of the product installation.

Helper views
^^^^^^^^^^^^

All news articles provide @@nitf and @@newsml views that are available
although are not registered.

Validating
^^^^^^^^^^

You can validate the output of the @@nitf and @@newsml views using services
like `XML validation`_.

You may use the `NITF Document Type Definition`_ version 3.5 and the `XHTML
Ruby Module`_ associated with it.

.. _`Dexterity`: http://pypi.python.org/pypi/plone.app.dexterity
.. _`IPTC`: http://www.iptc.org/
.. _`NewsCodes`: http://www.iptc.org/NewsCodes/
.. _`NewsML`: http://www.newsml.org/
.. _`NITF`: http://www.nitf.org/
.. _`NITF Document Type Definition`: http://www.iptc.org/std/NITF/3.5/specification/nitf-3-5.dtd
.. _`XHTML Ruby Module`: http://www.iptc.org/std/NITF/3.5/specification/xhtml-ruby-1.mod
.. _`XML validation`: http://www.xmlvalidation.com/
.. _`opening a support ticket`: https://github.com/collective/collective.nitf/issues
