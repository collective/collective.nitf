*** Settings ***

Resource  keywords.robot

Suite Setup  Open Test Browser
Suite Teardown  Close all browsers

*** Test cases ***

Test CRUD
    Enable Autologin as  Site Administrator
    Goto Homepage

    Create News Article
    Update
    Delete
