*** Variables ***

${PORT} =  55001
${ZOPE_URL} =  http://localhost:${PORT}
${PLONE_URL} =  ${ZOPE_URL}/plone
${BROWSER} =  Firefox

${front-page}  http://localhost:55001/plone/
${test-folder}  http://localhost:55001/plone/acceptance-test-folder


*** Keywords ***

Suite Setup
    Open browser  ${front-page}  browser=${BROWSER}  desired_capabilities=Capture Page Screenshot

Suite Teardown
    Close All Browsers

Log in
    [Documentation]  Log in to the site as ${userid} using ${password}. There
    ...              is no guarantee of where in the site you are once this is
    ...              done. (You are responsible for knowing where you are and
    ...              where you want to be)
    [Arguments]  ${userid}  ${password}

    Go to  ${PLONE_URL}/login_form
    Page should contain element  __ac_name
    Page should contain element  __ac_password
    Page should contain button  Log in
    Input text  __ac_name  ${userid}
    Input text  __ac_password  ${password}
    Click Button  Log in

Log in as site owner
    [Documentation]  Log in as the SITE_OWNER provided by plone.app.testing,
    ...              with all the rights and privileges of that user.
    Log in  ${SITE_OWNER_NAME}  ${SITE_OWNER_PASSWORD}

Log in as test user

    Log in  ${TEST_USER_NAME}  ${TEST_USER_PASSWORD}

Log out
    Go to  ${PLONE_URL}/logout
    Page should contain  logged out

Open Menu
    [Arguments]  ${elementId}

    Element Should Be Visible  css=dl#${elementId} span
    Element Should Not Be Visible  css=dl#${elementId} dd.actionMenuContent
    Click link  css=dl#${elementId} dt.actionMenuHeader a
    Wait until keyword succeeds  5s  1s  Element Should Be Visible  css=dl#${elementId} dd.actionMenuContent

Open Add New Menu
    Open Menu  plone-contentmenu-factories

Open Display Menu
    Open Menu  plone-contentmenu-display
