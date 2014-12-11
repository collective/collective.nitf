*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Variables  plone/app/testing/interfaces.py
Library  Remote  ${PLONE_URL}/RobotRemote

Suite Setup  Open Test Browser
Suite Teardown  Close all browsers

*** Variables ***

${ALT_ZOPE_HOST}  127.0.0.1
${ALT_PLONE_URL}  http://${ALT_ZOPE_HOST}:${ZOPE_PORT}/${PLONE_SITE_ID}
${LOCKED_MESSAGE}  This item was locked by admin 1 minute ago.
${title} =  Miracle Cure
${subtitle} =  Extra! Extra! Read all about it
${description} =  The Pinball Wizard in a miracle cure!
${byline} =  Newsboy
${body_html} =  <p>I'm free<br />I'm free<br />And freedom tastes of reality</p>

*** Test Cases ***

Test Locking Behavior
    Enable Autologin as  Owner
    Goto Homepage

    Click Add News Article
    Input Text  css=#form-widgets-IDublinCore-title  ${title}
    Input Text  css=#form-widgets-subtitle  ${subtitle}
    Input Text  css=#form-widgets-IDublinCore-description  ${description}
    Input Text  css=#form-widgets-byline  ${byline}

    Wait For Condition  return tinyMCE.activeEditor != null
    Execute Javascript  tinyMCE.activeEditor.setContent("${body_html}");

    Click Button  Save

    Go To  ${PLONE_URL}/miracle-cure
    Click Link  link=Edit

    # open a new browser to simulate a 2-user interaction
    Open Browser  ${ALT_PLONE_URL}
    Enable Autologin as  Site Administrator
    Go To  ${ALT_PLONE_URL}/miracle-cure
    Click Link  link=Edit
    Page Should Contain  Locked  ${LOCKED_MESSAGE}

    # FIXME: http://stackoverflow.com/q/27430323/644075
    # Switch Browser  1
    # Click Link  link=View
    # Page Should Not Contain  Locked  ${LOCKED_MESSAGE}

    # Switch Browser  2
    # Go To  ${PLONE_URL}/miracle-cure
    # Page Should Not Contain  Locked  ${LOCKED_MESSAGE}
    # Click Link  link=Edit

    # Switch Browser  1
    # Go To  ${PLONE_URL}/miracle-cure
    # Click Link  link=Edit
    # Page Should Contain  Locked  ${LOCKED_MESSAGE}

    # Switch Browser  2
    # Go To  ${PLONE_URL}/miracle-cure
    # Page Should Not Contain  Locked  ${LOCKED_MESSAGE}

*** Keywords ***

Click Add News Article
    Open Add New Menu
    Click Link  css=a#collective-nitf-content
    Page Should Contain  Add News Article
