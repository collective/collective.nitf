*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Variables  plone/app/testing/interfaces.py
Library  Remote  ${PLONE_URL}/RobotRemote

Suite Setup  Open Test Browser
Suite Teardown  Close all browsers

*** Variables ***

${title} =  Miracle Cure
${subtitle} =  Extra! Extra! Read all about it
${description} =  The Pinball Wizard in a miracle cure!
${byline} =  Newsboy
${body_html} =  <p>I'm free<br />I'm free<br />And freedom tastes of reality</p>

*** Test cases ***

Create News Article, subobjects and test views
    # FIXME: https://github.com/plone/plone.app.robotframework/issues/38
    [Tags]  Expected Failure

    Enable Autologin as  Site Administrator
    Go to Homepage

    Click Add News Article
    Input Text  css=#form-widgets-IDublinCore-title  ${title}
    Input Text  css=#form-widgets-subtitle  ${subtitle}
    Input Text  css=#form-widgets-IDublinCore-description  ${description}
    Input Text  css=#form-widgets-byline  ${byline}

    Wait For Condition  return tinyMCE.activeEditor != null
    Execute Javascript  tinyMCE.activeEditor.setContent("${body_html}");

    Click Button  Save
    Page Should Contain  Item created

    # A news article can contain images
    Open Add New Menu
    Click Link  css=a#image
    Page Should Contain  Add Image
    Choose File  css=#image_file  /tmp/img1.jpg
    Click Button  Save
    Page Should Contain  Changes saved

    # A news article can contain files
    Click Link  link=Miracle Cure
    Open Add New Menu
    Click Link  css=a#file
    Page Should Contain  Add File
    Choose File  css=#file_file  /tmp/txt1.txt
    Click Button  Save
    Page Should Contain  Changes saved

    # A news article can contain links
    Click Link  link=Miracle Cure
    Open Add New Menu
    Click Link  css=a#link
    Input Text  css=input[name=title]  An URL
    Input Text  css=#description  The description of the URL
    Input Text  css=#remoteUrl  http://foo.bar
    Click Button  Save
    Page Should Contain  Changes saved

    # Test views
    Go To  ${PLONE_URL}/miracle-cure
    Page Should Contain  Miracle Cure

    Go To  ${PLONE_URL}/miracle-cure/@@media
    page should Contain  Drag and drop images to change their order on the gallery

    Go To  ${PLONE_URL}/miracle-cure/@@galleria
    Page Should Contain  Miracle Cure

    Go To  ${PLONE_URL}/miracle-cure/@@nitf
    Page Should Contain  Miracle Cure

*** Keywords ***

Click Add News Article
    Open Add New Menu
    Click Link  css=a#collective-nitf-content
    Page Should Contain  Add News Article
