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
