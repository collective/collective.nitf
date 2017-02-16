Changelog
---------

There's a frood who really knows where his towel is.

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
.. _`Galleria`: http://galleria.io/
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
