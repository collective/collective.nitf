Changelog
---------

There's a frood who really knows where his towel is.

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
