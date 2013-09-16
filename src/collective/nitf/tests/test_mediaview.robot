*** Settings ***

Library  Selenium2Library  timeout=5 seconds  implicit_wait=3 seconds
Resource  keywords.robot
Resource  plone/app/robotframework/selenium.robot
Variables  plone/app/testing/interfaces.py

Suite Setup  Suite Setup
Suite Teardown  Suite Teardown

*** Variables ***

${img1_selector}  .ui-sortable #sortable-img1
${img2_selector}  .ui-sortable #sortable-img2
${img3_selector}  .ui-sortable #sortable-img3

*** Test cases ***

Test reorder
    Log in as site owner
    Click Link  link=n1
    Click Link  link=Media

    [Documentation]  Images in the original order.
	Page Should Contain Element  css=#sortable-img1.sort-0
	Page Should Contain Element  css=#sortable-img2.sort-1
	Page Should Contain Element  css=#sortable-img3.sort-2

    [Documentation]  Move 3th image to the left.
    Drag And Drop  css=${img3_selector}  css=.ui-sortable li:nth-of-type(1)
	Execute JavaScript 	window.update_sortable($('#sortable-img3'), -2)

    Click Link  link=Media

	Page Should Contain Element  css=#sortable-img3.sort-0
	Page Should Contain Element  css=#sortable-img1.sort-1
	Page Should Contain Element  css=#sortable-img2.sort-2

    Drag And Drop  css=${img1_selector}  css=.ui-sortable li:nth-of-type(3)
	Execute JavaScript 	window.update_sortable($('#sortable-img1'), 1)

    Click Link  link=Media

	Page Should Contain Element  css=#sortable-img3.sort-0
	Page Should Contain Element  css=#sortable-img2.sort-1
	Page Should Contain Element  css=#sortable-img1.sort-2
