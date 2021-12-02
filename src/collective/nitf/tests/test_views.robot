*** Settings ***

Resource  keywords.robot

Suite Setup  Open Test Browser
Suite Teardown  Close all browsers

*** Test cases ***

Test Edit image from Media
    Enable Autologin as  Site Administrator
    Go to Homepage

    Click Link  link=n1
    Click Link  link=Media

    # click on edit and wait until overlay is open
    Mouse Over  css=li#img1
    Wait Until Element Is Visible  css=li#img1 a.edit
    Click Link  css=li#img1 a.edit
    Wait Until Element Is Visible  css=.pattern-modal-buttons
    Click Button  css=.pattern-modal-buttons #form-buttons-save

Test Delete image from Media
    Enable Autologin as  Site Administrator
    Go to Homepage

    Click Link  link=n1
    Click Link  link=Media

    # click on trash icon and cancel
    Mouse Over  css=li#img1
    Wait Until Element Is Visible  css=li#img1 a.delete
    Click Link  css=li#img1 a.delete
    Wait Until Page Contains  Do you really want to delete this item?
    Wait Until Element Is Visible  css=.plone-modal-footer input[value=Cancel]
    Click Element  css=.plone-modal-footer input[value=Cancel]
    Page Should Contain Element  css=li#img1

    # click on trash icon and delete
    Wait Until Element Is Not Visible  css=.plone-modal-footer input[value=Cancel]
    Mouse Out  css=li#img1
    Mouse Over  css=li#img1
    Wait Until Element Is Visible  css=li#img1 a.delete
    Click Link  css=li#img1 a.delete
    Wait Until Page Contains  Do you really want to delete this item?
    Wait Until Element Is Visible  css=.plone-modal-footer input[value=Delete]
    Click Element  css=.plone-modal-footer input[value=Delete]
    Wait Until Page Does Not Contain Element  css=li#img1
    Reload Page
    Page Should Not Contain Element  css=li#img1

Test Change Views
    Enable Autologin as  Site Administrator
    Go to Homepage

    Click Link  link=n1
    Change View  Slideshow view
    Page Should Contain Element  css=.template-slideshow_view
    Change View  Text only view
    Page Should Contain Element  css=.template-text_only_view
    Change View  Default view
    Page Should Contain Element  css=.template-view

Test Media View Reorder
    Enable Autologin as  Site Administrator
    Go to Homepage

    Click Link  link=n1
    Click Link  link=Media

    # images in the original order
    Page Should Contain Element  css=#img1.sort-0
    Page Should Contain Element  css=#img2.sort-1
    Page Should Contain Element  css=#img3.sort-2

    # move 3th image to the left
    Drag And Drop By Offset  css=#img3.sort-2  -350  -10

    Click Link  link=Media

    Page Should Contain Element  css=#img3.sort-0
    Page Should Contain Element  css=#img1.sort-1
    Page Should Contain Element  css=#img2.sort-2

    Drag And Drop By Offset  css=#img1.sort-1  250  30

    Click Link  link=Media

    Page Should Contain Element  css=#img3.sort-0
    Page Should Contain Element  css=#img2.sort-1
    Page Should Contain Element  css=#img1.sort-2
