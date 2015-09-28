*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Variables  plone/app/testing/interfaces.py
Library  Remote  ${PLONE_URL}/RobotRemote

Suite Setup  Open Test Browser
Suite Teardown  Close all browsers

*** Test cases ***

Test Edit image from Media
    Enable Autologin as  Site Administrator
    Go to Homepage

    Click Link  link=n1
    Click Link  link=Media

    [Documentation]  Click on edit and wait until overlay is open
    Log Source
    Mouse Over  css=li#sortable-img1
    Click Link  css=li#sortable-img1 a.edit
    Wait Until Page Contains Element  css=form[name=edit_form]
    Click Button  Save

Test Delete image from Media
    # FIXME
    [Tags]  Expected Failure

    Enable Autologin as  Site Administrator
    Go to Homepage

    Click Link  link=n1
    Click Link  link=Media

    [Documentation]  Click on trash icon and cancel
    Mouse Over  css=li#sortable-img1
    Click Link  css=li#sortable-img1 a.delete
    Wait Until Page Contains  Do you really want to delete this item?
    Click Button  Cancel
    Click Link  link=Media
    Page Should Contain Element  css=li#sortable-img1

    [Documentation]  Click on trash icon and delete
    Mouse Over  css=li#sortable-img1
    Click Link  css=li#sortable-img1 a.delete
    Wait Until Page Contains  Do you really want to delete this item?
    Click Element  css=.pb-ajax input[value=Delete]
    ${timeout} =  Get Selenium Timeout
    ${implicit_wait} =  Get Selenium Implicit Wait
    Wait Until Keyword Succeeds  ${timeout}  ${implicit_wait}
    ...                          Page Should Not Contain Element  css=li#sortable-img1

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
    Drag And Drop  css=#sortable-img3.sort-2  css=#sortable li:nth-of-type(1)
    Execute JavaScript  window.update_sortable($('#sortable-img3'), -2)

    Click Link  link=Media

    Page Should Contain Element  css=#sortable-img3.sort-0
    Page Should Contain Element  css=#sortable-img1.sort-1
    Page Should Contain Element  css=#sortable-img2.sort-2

    Drag And Drop  css=#sortable-img1.sort-1  css=#sortable li:nth-of-type(3)
    Execute JavaScript  window.update_sortable($('#sortable-img1'), 1)

    Click Link  link=Media

    Page Should Contain Element  css=#sortable-img3.sort-0
    Page Should Contain Element  css=#sortable-img2.sort-1
    Page Should Contain Element  css=#sortable-img1.sort-2
