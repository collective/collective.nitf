*** Settings ***

Resource  keywords.robot

Suite Setup  Open Test Browser
Suite Teardown  Close all browsers

*** Test cases ***

Test Edit image from Media
    [Tags]  issue_172
    Enable Autologin as  Site Administrator
    Go to Homepage

    Click Link  link=n1
    Click Link  link=Media

    # click on edit and wait until overlay is open
    Mouse Over  css=li#sortable-img1
    Click Link  css=li#sortable-img1 a.edit
    Wait Until Page Contains Element  css=.pb-ajax form[name=edit_form]
    Click Button  Save

Test Delete image from Media
    Enable Autologin as  Site Administrator
    Go to Homepage

    Click Link  link=n1
    Click Link  link=Media

    # click on trash icon and cancel
    Mouse Over  css=li#sortable-img1
    Click Link  css=li#sortable-img1 a.delete
    Wait Until Page Contains  Do you really want to delete this item?
    Click Button  Cancel
    Click Link  link=Media
    Page Should Contain Element  css=li#sortable-img1

    # click on trash icon and delete
    Mouse Over  css=li#sortable-img1
    Click Link  css=li#sortable-img1 a.delete
    Wait Until Page Contains  Do you really want to delete this item?
    Click Element  css=.pb-ajax input[value=Delete]
    ${timeout} =  Get Selenium Timeout
    ${implicit_wait} =  Get Selenium Implicit Wait
    Wait Until Page Does Not Contain Element  css=li#sortable-img1

Test Change Views
    Enable Autologin as  Site Administrator
    Go to Homepage

    Click Link  link=n1
    Change View  Slideshow view
    Change View  Text only view
    Change View  Default view

Test Media View Reorder
    Enable Autologin as  Site Administrator
    Go to Homepage

    Click Link  link=n1
    Click Link  link=Media

    # images in the original order
    Page Should Contain Element  css=#sortable-img1.sort-0
    Page Should Contain Element  css=#sortable-img2.sort-1
    Page Should Contain Element  css=#sortable-img3.sort-2

    # move 3th image to the left
    Drag And Drop  css=#sortable-img3.sort-2  css=.ui-sortable li:nth-of-type(1)
    Execute JavaScript  window.update_sortable($('#sortable-img3'), -2)

    Click Link  link=Media

    Page Should Contain Element  css=#sortable-img3.sort-0
    Page Should Contain Element  css=#sortable-img1.sort-1
    Page Should Contain Element  css=#sortable-img2.sort-2

    Drag And Drop  css=#sortable-img1.sort-1  css=.ui-sortable li:nth-of-type(3)
    Execute JavaScript  window.update_sortable($('#sortable-img1'), 1)

    Click Link  link=Media

    Page Should Contain Element  css=#sortable-img3.sort-0
    Page Should Contain Element  css=#sortable-img2.sort-1
    Page Should Contain Element  css=#sortable-img1.sort-2
