Changelog
---------

There's a frood who really knows where his towel is.

3.0.0 (unreleased)
^^^^^^^^^^^^^^^^^^
.. Warning::
    For now, the upgrade steps was not been implemented to migrate ``collective.nitf``
    from Plone 4.3 to Plone 5.2. Version 3.0.0 should be installed on a Plone 5.2 that
    has never had ``collective.nitf`` installed before. It is recommended that migrations
    from Plone 4.3 to Plone 5.2 be done with
    `collective.transmogrifier <https://github.com/collective/collective.transmogrifier>`_ 
    or `collective.exportimport <https://github.com/collective/collective.exportimport>`_ .
    If you prefer to migrate via Plone migration, you will have to do the migration scripts
    to migrate ``collective.nitf``. Contributions here are welcome!

- Fix documentbyline viewlet in Plone 5.2.
  [wesleybl]

- Load Swiper with webpack.
  [wesleybl]

- Register internal static resources in Resource Registry.
  [wesleybl]

- Add suport to Python 3.7 and 3.8.
  [wesleybl]

- Remove dependency on unused package ``collective.prettydate``.
  [wesleybl]

- Remove dependency on plone.app.imaging.
  [wesleybl]

- Drop support to Plone 4.3 and Plone 5.1.
  [wesleybl]

- Remove old upgrade steps.
  [wesleybl]


2.1.1 (2021-04-15)
^^^^^^^^^^^^^^^^^^

- Add a transaction note for upgradeStep v2003, available at `Undo` tab in `/` in the ZMI, to make review easier after running since it can modify thousands of objects. (complements `#232`_).
  [idgserpro]


2.1.0 (2020-12-23)
^^^^^^^^^^^^^^^^^^

.. Warning::
    This version disables usage of Latest Sectionable NITF portlet.
    Remove manually all Latest Sectionable NITF portlets before upgrading.
    This version removes tile registration/removal;
    you must depend on plone.app.tiles >= 3.0.0 to avoid issues with ``collective.nitf`` tile.

- Remove SearchableText from metadata of catalog (fix `#232`_).
  [idgserpro]

- Fix rendering plone.belowcontenttitle.contents when adding a Link or a File inside a nitf content and plone.app.contenttypes is installed (fix `#228`_)
  [idgserpro]

- Fix AttributeError: query when running upgradeStep 1008 (fix `#226`_)
  [idgserpro]

- Fix error when creating Plone Site, when collective.nitf is available (fix `#233`_).
  [idgserpro]

- Remove dependency on Cycle2;
  If you don't have other package depending on collective.js.cycle2 you are safe to uninstall it (closes `#200`_).
  [rodfersou]

- Remove needless tile registration/removal when using plone.app.tiles >= 3.0.0.
  [hvelarde]

- Manage deprecation of CMFQuickInstallerTool on Plone >= 5.1;
  [hvelarde]

- Better handling of package uninstall.
  [hvelarde]

- Fix package dependencies.
  [hvelarde]

- Small code refactor to increase future Python 3 compatibility;
  add dependency on `six <https://pypi.python.org/pypi/six>`_.
  [hvelarde]

- Latest Sectionable NITF portlet was disabled and will be completely removed in version 3.0.
  [hvelarde]


2.1b4 (2017-10-18)
^^^^^^^^^^^^^^^^^^

- ``SearchableText`` index for News Article content type now includes object keywords (fixes `brasil.gov.portal#155 <https://github.com/plonegovbr/brasil.gov.portal/issues/155>`_).
  [hvelarde]


2.1b3 (2017-07-05)
^^^^^^^^^^^^^^^^^^

- Add NITF tile for collective.cover when upgrading to 2.x (closes `#205`_).
  [idgserpro]


- Remove ``relatable_content_types`` registry record when upgrading to 2.x (closes `#208`_).
  [idgserpro]


2.1b2 (2017-06-12)
^^^^^^^^^^^^^^^^^^

- Do not create a link to ``None`` on the tile.
  [hvelarde]

- Fix upgrade process between versions 1.x and 2.x;
  check documentation on migration for more information (closes `#198`_).
  [rodfersou, hvelarde]


2.1b1 (2017-02-16)
^^^^^^^^^^^^^^^^^^

- Handle corner case when upgrade step for 1008 found a collection with no query defined.
  [hvelarde]

- Simplify slideshow template to avoid depending on context id;
  this solves an issue when id ends with ".html".
  [rodfersou]

- Refactor static resources.
  [rodfersou]

- Add classes to HTML elements on tile for easy visual customization.
  [agnogueira]

- Remove dependency on plone.directives.form and latest traces of Grok.
  [hvelarde]

- Fix exception getting image size with ``ImageScaling`` adapter (refs. `sc.social.like #87`_).
  [rodfersou]


2.0b4 (2016-11-03)
^^^^^^^^^^^^^^^^^^

- Do not try to create scales on news article with no lead image;
  this was causing issues in some Collection view methods and in collective.cover's Collection tile (fixes `#178`_).
  [hvelarde]


2.0b3 (2016-09-12)
^^^^^^^^^^^^^^^^^^

- Fix issue in NITF tile that was causing an exception when dropping content into it (fixes `#175`_).
  [rodfersou]


2.0b2 (2016-07-27)
^^^^^^^^^^^^^^^^^^

- The ``getImage()`` and ``imageCaption()`` methods of the ``NITF`` class are deprecated and will be removed on next release;
  use ``image()`` and ``media_caption()`` instead.
  [hvelarde]

- Fix issue with ``collective.nitf.image`` viewlet raising ``AttributeError`` when plone.app.contenttypes is installed (closes `#169`_).
  [hvelarde]

- Use ``<p>`` tag to display the News Article subtitle to avoid warnings on validation.
  [hvelarde]

- Fix exception when syndicalize NITF (closes `#161`_).
  [rodfersou]

- Fix tile date format.
  [hvelarde]

- Avoid rising exceptions when content referenced in tile is not available (fixes `#154`_).
  [hvelarde, rodfersou]

- Remove hard dependency on plone.app.referenceablebehavior as Archetypes is no longer the default framework in Plone 5.
  Under Plone < 5.0 you should now explicitly add it to the `eggs` part of your buildout configuration to avoid issues while upgrading.
  [hvelarde]


2.0b1 (2016-02-29)
^^^^^^^^^^^^^^^^^^

- Show title of news article as ``alt`` attribute on tile's image.
  [hvelarde]

- Fix upgrade step to work with both, Archetypes and Dexterity-based collections.
  [rodfersou]


2.0a1 (2015-09-30)
^^^^^^^^^^^^^^^^^^

.. Warning::
    Upgrades are supported only from release 1.0b3.

- Make control panel configlet accesible to Site Administrator role (closes `#137`_).
  [hvelarde]

- Load Cycle2 resources from the JS registry if available (closes `#133`_).
  [hvelarde]

- Fix display of byline and refactor override of ``documentbyline`` viewlet;
  avoid performance issues when having many users by memoizing expensive call to Membership tool (fixes `#128`_).
  [hvelarde, rodfersou]

- Replace slideshow framework machinery;
  we use `Cycle2`_ now instead of `Galleria`_.
  Don't forget do uninstall and remove collective.js.galleria if you no longer depend on it on your site (closes `#116`_).
  [rodfersou, hvelarde]

- Fix default values for genre and urgency fields (closes `#118`_).
  [rodfersou]

- Add NITF tile for collective.cover (closes `#123`_).
  [hvelarde]

- Reimplement section field as a behavior (closes `#98`_).
  [hvelarde]

- Drop support of Plone 4.2.
  [hvelarde]

- Remove dependency on collective.z3cform.widgets.
  Don't forget do uninstall and remove the package if you no longer depend on it on your site.
  [hvelarde]

- Update package i18n and Spanish and Brazilian Portuguese translations.
  [hvelarde]

- Restore default binding on Link content type at uninstall time.
  [hvelarde]

- Add ``Current`` as default value for available_genres and ``General`` as
  default value for available_sections.
  [hvelarde]

- Character counter code was removed from package; this should be
  reimplemented using collective.js.charcount (closes `#75`_).
  [hvelarde]

- Package was cleaned by removing some dependencies,
  deprecated methods on default view,
  unused macros from templates,
  and needless resources, scripts and styles.
  [marcosfromero, hvelarde]

- Remove all javascript from templates, create new nitf.js and use
  jsregistry (closes `#94`_). [marcosfromero]

- Add confirmation overlay before removing an image in media.pt
  (closes `#85`_). [marcosfromero]

- Add required script library in media.pt to prevent image not loading
  when editing in overlay (closes `#84`_). [marcosfromero]

- Fields were reordered to enhance user experience on adding/editing content:
  'location' field is now above 'body text' and 'urgency' is below 'genre'.
  [hvelarde]

- Reimplement ``keywords`` and ``documentbyline`` viewlets with semantic markup and
  support for news article byline for INITF interface.
  [jpgimenez, hvelarde, cleberjsantos]

- Refactor templates to implement semantic markup to annotate news-specific
  metadata using rNews, schema.org and RDFa (closes `#47`_).
  [jpgimenez, marcosfromero, hvelarde]

- Add plone.app.relationfield as a dependency; this is needed for Dexterity
  to proper handle relations (closes `#71`_). [jpgimenez]

- Remove five.grok dependency, will easy the mainteinance and the
  extendibility of the package. [jpgimenez]

- Changes image link behavior in view.pt for mobile devices
  (closes `#62`_). [marcosfromero]


.. _`Cycle2`: http://jquery.malsup.com/cycle2/
.. _`Galleria`: https://galleriajs.github.io
.. _`sc.social.like #87`: https://github.com/collective/sc.social.like/issues/87
.. _`#47`: https://github.com/collective/collective.nitf/issues/47
.. _`#62`: https://github.com/collective/collective.nitf/issues/62
.. _`#71`: https://github.com/collective/collective.nitf/issues/71
.. _`#75`: https://github.com/collective/collective.nitf/issues/75
.. _`#84`: https://github.com/collective/collective.nitf/issues/84
.. _`#85`: https://github.com/collective/collective.nitf/issues/85
.. _`#94`: https://github.com/collective/collective.nitf/issues/94
.. _`#98`: https://github.com/collective/collective.nitf/issues/98
.. _`#116`: https://github.com/collective/collective.nitf/issues/116
.. _`#118`: https://github.com/collective/collective.nitf/issues/118
.. _`#123`: https://github.com/collective/collective.nitf/issues/123
.. _`#128`: https://github.com/collective/collective.nitf/issues/128
.. _`#133`: https://github.com/collective/collective.nitf/issues/133
.. _`#137`: https://github.com/collective/collective.nitf/issues/137
.. _`#154`: https://github.com/collective/collective.nitf/issues/154
.. _`#161`: https://github.com/collective/collective.nitf/issues/161
.. _`#169`: https://github.com/collective/collective.nitf/issues/169
.. _`#175`: https://github.com/collective/collective.nitf/issues/175
.. _`#178`: https://github.com/collective/collective.nitf/issues/178
.. _`#198`: https://github.com/collective/collective.nitf/issues/198
.. _`#200`: https://github.com/collective/collective.nitf/issues/200
.. _`#205`: https://github.com/collective/collective.nitf/issues/205
.. _`#208`: https://github.com/collective/collective.nitf/issues/208
.. _`#226`: https://github.com/collective/collective.nitf/issues/226
.. _`#228`: https://github.com/collective/collective.nitf/issues/228
.. _`#232`: https://github.com/collective/collective.nitf/issues/232
.. _`#233`: https://github.com/collective/collective.nitf/issues/233
