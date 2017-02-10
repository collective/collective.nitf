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

Internals
---------

``collective.nitf`` uses Cycle2 slideshow plugin for jQuery and it can load its resources from the Plone JS registry if they are present there.

If you're using ``collective.nitf`` with other packages that use Cycle2 also (like `sc.photogallery`_ or `covertile.cycle2`_),
it is highly recommended that you register those resources to load them once and avoid conflicts.

You can use a ``jsregistry.xml`` file that includes the following:

.. code-block:: xml

    <javascript id="++resource++collective.js.cycle2/jquery.cycle2.min.js"
        cacheable="True" compression="none" cookable="True" enabled="True" />
    <javascript id="++resource++collective.js.cycle2/jquery.cycle2.carousel.min.js"
        cacheable="True" compression="none" cookable="True" enabled="True" />
    <javascript id="++resource++collective.js.cycle2/jquery.cycle2.swipe.min.js"
        cacheable="True" compression="none" cookable="True" enabled="True" />

.. _`sc.photogallery`: https://pypi.python.org/pypi/sc.photogallery
.. _`covertile.cycle2`: https://pypi.python.org/pypi/covertile.cycle2

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
