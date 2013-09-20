*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Library  Remote  ${PLONE_URL}/RobotRemote

Suite Setup  Open Test Browser
Suite Teardown  Close all browsers

*** Test cases ***

Test Change views
    Enable Autologin as  Site Administrator
    Go to Homepage

    Click Link  link=n1
    Page Should Not Contain Element  id=mediabox
    Go To  ${PLONE_URL}/n1/select_default_view
    Select Radio Button  templateId  nitf_galleria
    Click Button  Save
    Page Should Contain  View changed.
    Page Should Contain Element  id=mediabox
    Go To  ${PLONE_URL}/n1/select_default_view
    Select Radio Button  templateId  view
    Click Button  Save
    Page Should Contain  View changed.
    Page Should Not Contain Element  id=mediabox
    Click Link  id=parent-fieldname-image
    Log Source
    Wait Until Page Contains Element  css=.pb-ajax .galleria-image img

Test Media View Reorder
    # FIXME
    [Tags]  Expected Failure

    Enable Autologin as  Site Administrator
    Go to Homepage

    Click Link  link=n1
    Click Link  link=Media

    [Documentation]  Images in the original order.
    Page Should Contain Element  css=#sortable-img1.sort-0
    Page Should Contain Element  css=#sortable-img2.sort-1
    Page Should Contain Element  css=#sortable-img3.sort-2

    [Documentation]  Move 3th image to the left.
    Drag And Drop  css=${img3_selector}  css=.ui-sortable li:nth-of-type(1)
    Execute JavaScript  window.update_sortable($('#sortable-img3'), -2)

    Click Link  link=Media

    Page Should Contain Element  css=#sortable-img3.sort-0
    Page Should Contain Element  css=#sortable-img1.sort-1
    Page Should Contain Element  css=#sortable-img2.sort-2

    Drag And Drop  css=${img1_selector}  css=.ui-sortable li:nth-of-type(3)
    Execute JavaScript  window.update_sortable($('#sortable-img1'), 1)

    Click Link  link=Media

    Page Should Contain Element  css=#sortable-img3.sort-0
    Page Should Contain Element  css=#sortable-img2.sort-1
    Page Should Contain Element  css=#sortable-img1.sort-2
