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

.. image:: http://img.shields.io/pypi/v/collective.nitf.svg
    :target: https://pypi.python.org/pypi/collective.nitf

.. image:: https://img.shields.io/travis/collective/collective.nitf/master.svg
    :target: http://travis-ci.org/collective/collective.nitf

.. image:: https://img.shields.io/coveralls/collective/collective.nitf/master.svg
    :target: https://coveralls.io/r/collective/collective.nitf

Got an idea? Found a bug? Let us know by `opening a support ticket`_.

Don't Panic
-----------

Installation
^^^^^^^^^^^^

To enable this product in a buildout-based installation:

#. Edit your buildout.cfg and add ``collective.nitf`` to the list of eggs to install::

    [buildout]
    ...
    eggs =
        collective.nitf

After updating the configuration you need to run ''bin/buildout'', which will take care of updating your system.

Go to the 'Site Setup' page in a Plone site and click on the 'Add-ons' link.

Check the box next to ``collective.nitf`` and click the 'Activate' button.

Upgrading from 1.x to 2.x
^^^^^^^^^^^^^^^^^^^^^^^^^

.. Warning::
    Upgrades to version 2.x are only supported from latest version of branch 1.x.

You have to be aware of the following changes when migrating from version 1.x to 2.x:

* Package is no longer compatible with Plone 4.2
* Latest Sectionable NITF portlet was disabled and will be completely removed in version 3.0;
  you should remove all Latest Sectionable NITF portlets from your site before upgrading
* Package no longer depends on Grok
* Package no longer depends on `collective.z3cform.widgets <http://pypi.python.org/pypi/collective.z3cform.widgets>`_;
  you should uninstall that dependency manually if there is no other package depending on it on your site
* Package no longer depends on `plone.app.referenceablebehavior <http://pypi.python.org/pypi/plone.app.referenceablebehavior>`_;
  the ``IReferenceable`` behavior included there is no longer assigned by default
* The character counter is no longer available
* We use `Swiper <http://idangero.us/swiper/>`_ as the framework for the slideshow view.
* The following views are available for a News Article: ``view``, ``slideshow_view`` and ``text_only_view``
* View templates were completely refactored and support for semantic markup was added;
  the default view displays a bigger image
* The following behaviors are assigned by default to the News Article content type: ``plone.app.relationfield.behavior.IRelatedItems`` and ``collective.nitf.behaviors.interfaces.ISection``
* A new permission ``collective.nitf: Setup`` is available to access the control panel configlet and is assigned by default to ``Manager`` and ``Site Administrator`` roles
* Static resources are now named ``nitf.css`` and ``nitf.js`` (easier to debug at the browser)

An upgrade step is available to remove old resources, rename the views, and reindex all News Articles to reflect changes.
The upgrade step will not remove the ``plone.app.referenceablebehavior.referenceable.IReferenceable`` behavior if applied.

Behaviors
^^^^^^^^^

This package includes a behavior called ``collective.nitf.behaviors.interfaces.ISection``.
By applying it to a Dexterity-based content type you will get a new field called ``section``.

Helper views
^^^^^^^^^^^^

All news articles provide @@nitf and @@newsml views that are available although are not registered.

You can validate the output of the those views using services like `XML validation`_.

You may use the `NITF Document Type Definition`_ version 3.5 and the `XHTML Ruby Module`_ associated with it.

.. _`IPTC`: http://www.iptc.org/
.. _`NewsCodes`: http://www.iptc.org/NewsCodes/
.. _`NewsML`: http://www.newsml.org/
.. _`NITF`: http://www.nitf.org/
.. _`NITF Document Type Definition`: http://www.iptc.org/std/NITF/3.5/specification/nitf-3-5.dtd
.. _`XHTML Ruby Module`: http://www.iptc.org/std/NITF/3.5/specification/xhtml-ruby-1.mod
.. _`XML validation`: http://www.xmlvalidation.com/
.. _`opening a support ticket`: https://github.com/collective/collective.nitf/issues

Development
^^^^^^^^^^^

We use Webpack to process static resources on this package.
Webpack processes LESS and JS files, minifies the resulting CSS and JS, and optimizes all images.
The final JS file is also a UMD package, which provides compatibility with most popular script loaders.

To contribute, you should start the instance in one shell and start Webpack watcher on another with the following command:

.. code-block:: bash

    $ bin/npm_watch

Then go to ``webpack/app`` folder and edit LESS and JS files;
Webpack watcher will automatically create the final resources in the right place.

There are also other commands added to handle more complex scenarios.
The following command will set the buildout node installation in the system PATH, this way you can use Webpack as described on Webpack docs.

.. code-block:: bash

    $ bin/webpack_env

The following command generates JS and CSS without the minify step (it can be used to check the code being generated in a human readable way).

.. code-block:: bash

    $ bin/npm_dev

The following command rebuilds static files and exit (insted of keep watching the changes):

.. code-block:: bash

    $ bin/npm_build
