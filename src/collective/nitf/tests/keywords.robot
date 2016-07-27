*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Variables  plone/app/testing/interfaces.py
Library  Remote  ${PLONE_URL}/RobotRemote

*** Variables ***

${title_selector} =  input#form-widgets-IDublinCore-title
${description_selector} =  textarea#form-widgets-IDublinCore-description
${file_field_selector} =  //input[@id="file_file" or @id="form-widgets-file-input"]
${image_field_selector} =  //input[@id="image_file" or @id="form-widgets-image-input"]
${title} =  Miracle Cure
${subtitle} =  Extra! Extra! Read all about it
${description} =  The Pinball Wizard in a miracle cure!
${byline} =  Newsboy
${body_html} =  <p>I'm free<br></br>I'm free<br></br>And freedom tastes of reality</p>
${body_html_text_1} =  I'm free
${body_html_text_2} =  And freedom tastes of reality

*** Keywords ***

Click Add News Article
    Open Add New Menu
    Click Link  css=a#collective-nitf-content
    Page Should Contain  Add News Article

Create News Article
    Click Add News Article
    Input Text  css=${title_selector}  ${title}
    Input Text  css=#form-widgets-subtitle  ${subtitle}
    Input Text  css=${description_selector}  ${description}
    Input Text  css=#form-widgets-byline  ${byline}

    Wait For Condition  return tinyMCE.activeEditor != null
    Execute Javascript  tinyMCE.activeEditor.setContent("${body_html}");

    Click Button  Save
    Page Should Contain  Item created
    # all elements must be visible on the view
    Page Should Contain  ${title}
    Page Should Contain  ${subtitle}
    Page Should Contain  ${description}
    Page Should Contain  ${byline}
    Page Should Contain  ${body_html_text_1}
    Page Should Contain  ${body_html_text_2}

    # A news article can contain images
    Open Add New Menu
    Click Link  css=a#image
    Page Should Contain  Add Image
    Choose File  xpath=${image_field_selector}  /tmp/640px-Mandel_zoom_00_mandelbrot_set.jpg
    Click Button  Save
    Page Should Contain  Changes saved

    # A news article can contain files
    Click Link  link=Miracle Cure
    Open Add New Menu
    Click Link  css=a#file
    Page Should Contain  Add File
    Choose File  xpath=${file_field_selector}  /tmp/random.txt
    Click Button  Save
    Page Should Contain  Changes saved

    # A news article can contain links
    Click Link  link=Miracle Cure
    Open Add New Menu
    Click Link  css=a#link
    Input Text  css=#title  An URL
    Input Text  css=#description  The description of the URL
    Input Text  css=#remoteUrl  http://foo.bar
    Click Button  Save
    Page Should Contain  Changes saved

    Click Link  link=Miracle Cure

Update
    Click Link  link=Edit
    Click Button  Save
    Page Should Contain  Changes saved

Delete
    Open Action Menu
    Click Link  css=a#plone-contentmenu-actions-delete
    Click Button  Delete
    Page Should Contain  Plone site

Change View
    [arguments]  ${view}

    Open Display Menu
    Click Link  link=${view}
    Page Should Contain  View changed
