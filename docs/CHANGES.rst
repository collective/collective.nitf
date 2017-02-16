There's a frood who really knows where his towel is
---------------------------------------------------

1.0b10 (2017-02-16)
^^^^^^^^^^^^^^^^^^^

- Fix brown bag release.
  [hvelarde]


1.0b9 (2017-02-16)
^^^^^^^^^^^^^^^^^^

- Handle corner case when upgrade step for 1008 found a collection with no query defined.
  [hvelarde]


1.0b8 (2015-10-16)
^^^^^^^^^^^^^^^^^^

- Fix upgrade step to work with both, Archetypes and Dexterity-based collections.
  [rodfersou]

- Use "application/javascript" media type instead of the obsolete "text/javascript".
  [hvelarde]


1.0b7 (2015-10-01)
^^^^^^^^^^^^^^^^^^

- Hide profiles used on upgrade steps (closes `#143`_).
  [winstonf88]


1.0b6 (2015-09-30)
^^^^^^^^^^^^^^^^^^

- Fix AttributeError on upgrade step (closes `#139`_).
  [winstonf88, rodfersou]

- Byline field honored in syndication (closes `#93`_).
  [rodfersou]


1.0b5 (2015-05-01)
^^^^^^^^^^^^^^^^^^

- Fix urgency field filter for Collections (closes `#111`_).
  [rodfersou]


1.0b4 (2014-12-26)
^^^^^^^^^^^^^^^^^^^^^^

- Add locking behaviour. [rodfersou]


1.0b3 (2013-07-23)
^^^^^^^^^^^^^^^^^^

- Remove unused gallery_viewlet template. [hvelarde]

- Fix @@images view to proper use all the params it receives [ericof]

- Changes galleria debug to off mode. [cleberjsantos]

- Fix galleria view with large image. [cleberjsantos]


1.0b2 (2013-05-02)
^^^^^^^^^^^^^^^^^^

- Update Brazilian Portuguese translation. [hvelarde]

- Fix image scaling of Dexterity images. [ericof]

- Cleanup Galleria code; add title and description (when available). [ericof]

- Fix character counter selector. [cleberjsantos]


1.0b1 (2013-04-17)
^^^^^^^^^^^^^^^^^^

- News Article now support plone.app.contenttypes [ericof]

- Remove default and missing_value attributes from text field, this is
  causing problems with the RichText widget in Plone 4.3, now that is
  handled in the indexer. [jpgimenez]

- Package is now Dexterity 2.0 and Plone 4.3 compatible (closes `#52`_).
  [jpgimenez, hvelarde]

- Remove needless registration of TokenInputFieldWidget now made at
  installation time of collective.z3cform.widgets in new release 1.0b6.
  [hvelarde]

- Upgrade step to fix content created before the setting of widgets default
  values (closes `#49`_). [jpgimenez]

- Fix for summary_view with NITF content inside. [jpgimenez]

- Remove old js code to collapse edit form. [jpgimenez]

- Support image traversal. [jpgimenez]

- Use galleria.io for image galleries with a custom theme. [jpgimenez]

- Move the gallery to an overlay and load the images with ajax. [jpgimenez]

- Package is no longer compatible with Plone 4.1. [hvelarde]

- Do not show the folder listing if there are no files or links inside the
  News Article. [hvelarde]

- Initial Brazilian Portuguese translation. [agnogueira]

- NITF content type does not implement INonStructuralFolder any longer to
  allow folder factories menu. [jpgimenez]

- Add Pillow as a dependency of the package. [hvelarde]

- PEP8 fixes. [ericof]

- Create named vocabularies for Genres and Urgencies. [ericof]

- Vocabularies terms are now shown sorted; tests added. [hvelarde]

- Replaced the UserFriendlyTypes vocabulary in favor of
  ReallyUserFriendlyTypes. [frapell]

- Control panel fields sections and possible_genres were renamed to
  available_sections and available_genres; some code refactoring for better
  readability; tests were updated. [hvelarde]

- Added a field to the control panel to set the relatable content types; tests
  were updated. [hvelarde]

- Add-on layer was renamed to INITFLayer. [hvelarde]

- Change relatedItem widget to use MultiContentSearchFieldWidget. [flecox]

- Adds support to new-style Collections. [davilima6]

- Added charcount functionality for title and description [quimera]

- fix alternative view for news articles. [cleberjsantos]


1.0a3 (2012-07-06)
^^^^^^^^^^^^^^^^^^

- Make the NITF object to provide the INonStructuralFolder interface so
  comments can be added to them. [frapell]


1.0a2 (2012-06-18)
^^^^^^^^^^^^^^^^^^

- Dependency package collective.prettydate no longer has a GS profile.
  [hvelarde]

- Indexes are now installed in an alternate way so catalog information is not
  lost on package reinstall (fixes `#33`_). [hvelarde]

- Spanish translation of News Codes was updated. [hvelarde]


1.0a1 (2012-05-21)
^^^^^^^^^^^^^^^^^^

- Initial release.

.. _`#33`: https://github.com/collective/collective.nitf/issues/33
.. _`#49`: https://github.com/collective/collective.nitf/issues/49
.. _`#52`: https://github.com/collective/collective.nitf/issues/52
.. _`#93`: https://github.com/collective/collective.nitf/issues/93
.. _`#111`: https://github.com/collective/collective.nitf/issues/111
.. _`#139`: https://github.com/collective/collective.nitf/issues/139
.. _`#143`: https://github.com/collective/collective.nitf/issues/143
