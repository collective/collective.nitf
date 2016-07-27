*** Settings ***

Resource  keywords.robot
Resource  Accessibility/wavetoolbar.robot

Suite Setup  Run Keywords
...  Open Accessibility Test Browser  Maximize Browser Window
Suite Teardown  Close All Browsers

*** Test cases ***

Test A11Y
    [Tags]  issue_172
    [Documentation]  Test content type views for accessibility errors.

    Enable Autologin as  Site Administrator
    Go to Homepage

    Create News Article
    Check A11Y Errors  0
    Change View  Slideshow view
    Check A11Y Errors  0
    Change View  Text only view
    Check A11Y Errors  0

Test Media A11Y
    Enable Autologin as  Site Administrator
    Go to Homepage

    Click Link  link=n1
    Click Link  link=Media
    Check A11Y Errors  0

*** Keywords ***

Check A11Y Errors
    [Arguments]  ${max}

    ${url} =  Execute Javascript  window.location.href;

    ${errors} =  Count WAVE accessibility errors  ${url}
    Should be true  ${errors} <= ${max}
    ...  WAVE Toolbar reported ${errors} errors for ${url}
