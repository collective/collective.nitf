There's a frood who really knows where his towel is
---------------------------------------------------

1.0b4 (unreleased)
^^^^^^^^^^^^^^^^^^

- Remove HiddenProfiles utility; that's most likely the job of a policy
  package. [hvelarde]

- Remove updateWidgets method on Add and Edit forms as they were used only to
  style them; we should implement this on CSS if needed. [hvelarde]

- Remove five.grok dependency, will easy the mainteinance and the
  extendibility of the package. [jpgimenez]

- Semantic markup in galleria template. [marcosfromero]

- Test for changes in default view. [marcosfromero]

- Needless override on folder_summary_view that was causing ``AttributeError:
  'View' object has no attribute 'images'`` was removed. [hvelarde]

- Reimplement keywords and document_byline viewlets with semantic markup and
  support for news article byline for INITF interface.
  [jpgimenez, hvelarde, cleberjsantos]

- Implement semantic markup to annotate news-specific metadata using
  schema.org and RDFa (closes `#47`_). [jpgimenez, hvelarde]

- Changes image link behavior in view.pt for mobile devices 
  (closes `#62`_). [marcosfromero]


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
.. _`#47`: https://github.com/collective/collective.nitf/issues/47
.. _`#49`: https://github.com/collective/collective.nitf/issues/49
.. _`#52`: https://github.com/collective/collective.nitf/issues/52
.. _`#62`: https://github.com/collective/collective.nitf/issues/62