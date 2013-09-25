*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Library  Remote  ${PLONE_URL}/RobotRemote

Suite Setup  Open Test Browser
Suite Teardown  Close all browsers

*** Test cases ***

Create News Article, subobjects and test views
    Enable Autologin as  Site Administrator
    Go to Homepage

    Open Add New Menu
    Click Link  css=a#collective-nitf-content
    Page Should Contain  Add News Article
    Input Text  css=#form-widgets-IDublinCore-title  Miracle Cure
    Input Text  css=#form-widgets-subtitle  Extra! Extra! Read all about it 
    Input Text  css=#form-widgets-IDublinCore-description  The Pinball Wizard in a miracle cure!
    Input Text  css=#form-widgets-byline  Newsboy

    # FIXME: populate body field without JS
    #Wait For Condition  return tinyMCE.activeEditor != null
    #Execute Javascript  tinyMCE.activeEditor.setContent("<p>I'm free<br />I'm free<br />And freedom tastes of reality</p>");

    Click Link  link=Categorization
    Select From List  css=#form-widgets-section  Tommy
    Select From List  css=#form-widgets-genre  Current
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

    Go To  ${PLONE_URL}/miracle-cure/@@nitf_galleria
    Page Should Contain  Miracle Cure

    Go To  ${PLONE_URL}/miracle-cure/@@nitf
    Page Should Contain  Miracle Cure
