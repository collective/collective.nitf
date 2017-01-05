*** Settings ***

Resource  keywords.robot

Suite Setup  Open Test Browser
Suite Teardown  Close all browsers

*** Test cases ***

Test CRUD
    [Tags]  issue_172
    Enable Autologin as  Site Administrator
    Goto Homepage

    Create News Article
    Update
    Delete

Test Folder Full View
    Enable Autologin as  Site Administrator
    Go to Homepage

    Open Add New Menu
    Click Link  css=a#folder
    Page Should Contain  Add Folder
    Input Text  css=#form-widgets-IDublinCore-title,#title  Test Folder
    Click Button  Save
    Page Should Contain  Test Folder

    Click Add News Article
    Input Text  css=#form-widgets-IDublinCore-title  ${title}
    Input Text  css=#form-widgets-IDublinCore-description  ${description}
    Input Text  css=#form-widgets-byline  ${byline}
    Wait For Condition  return tinyMCE.activeEditor != null
    Execute Javascript  tinyMCE.activeEditor.setContent("${body_html}");
    Click Button  Save
    Page Should Contain  Item created

    Click Link  link=Test Folder
    Open Display Menu
    Click Link  link=All content
    Check Status Message  View changed

    # all elements must be visible on the view
    Page Should Contain  ${title}
    Page Should Contain  ${description}
    Page Should Contain  ${byline}
    Page Should Contain  ${body_html_text_1}
    Page Should Contain  ${body_html_text_2}
