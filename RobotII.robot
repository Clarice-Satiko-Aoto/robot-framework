*** Settings ***
Documentation       Orders robots from RobotSpareBin Industries Inc.
...                 Saves the order HTML receipt as a PDF file.
...                 Saves the screenshot of the ordered robot.
...                 Embeds the screenshot of the robot to the PDF receipt.
...                 Creates ZIP archive of the receipts and the images.

Library             RPA.Browser.Selenium    auto_close=${FALSE}
Library             RPA.HTTP
Library             RPA.PDF
Library             RPA.Desktop
Library             RPA.Tables
Library             RPA.Archive
Library             RPA.FileSystem


*** Variables ***
${pdf_directory}        ./pdf
${image_directory}      ./img
${output_directory}     ./output


*** Tasks ***
# Order robots from RobotSpareBin Industries Inc
#    Open the robot order website
#    Download the csv file
#    Accept pop up and get order from the csv file
#    [Teardown]    Close the browser

Create a ZIP file of receipt PDF files
    To create zip file


*** Keywords ***
# Open the robot order website
#    Open Available Browser    https://robotsparebinindustries.com/#/robot-order

# Download the csv file
#    Download    https://robotsparebinindustries.com/orders.csv    overwrite=True

# Get one order
#    [Arguments]    ${order}
#    Select From List By Value    head    ${order}[Head]
#    Click Element    id-body-${order}[Body]
#    Input Text    //input[@placeholder='Enter the part number for the legs']    ${order}[Legs]
#    Input Text    //input[@placeholder='Shipping address']    ${order}[Address]
#    Run Keyword And Ignore Error    Wait And Click Button    //*[@id="order"]
#    ${STATUS}    Run Keyword And Continue On Failure
#    ...    Run Keyword And Return Status
#    ...    Wait And Click Button
#    ...    //*[@id="order"]
#    Run Keyword If "${STATUS}" == "FAIL"    Click Button    //*[@id="order"]

# Accept pop up and get order from the csv file
#    ${orders}    Read table from CSV    orders.CSV

#    FOR    ${order}    IN    @{orders}
#    Run Keyword And Ignore Error    Click Button    Yep
#    Run Keyword And Ignore Error    Get one order    ${order}
#    Run Keyword And Ignore Error    Wait Until Element Is Visible    //*[@id='receipt']    20s
#    Run Keyword And Ignore Error    Wait Until Page Contains Element    //*[@id='receipt']    10s
#    Run Keyword And Ignore Error    Wait Until Element Is Visible    id:robot-preview-image
#    ${pdf}    Get Element Attribute    //*[@id='receipt']    outerHTML
#    Html To Pdf    ${pdf}    ${pdf_directory}/${order}[Order number].pdf
#    ${output_file}    Set Variable    ${pdf_directory}/${order}[Order number].pdf

#    # Abrir o PDF
#    Open Pdf    ${output_file}

#    Screenshot    //*[@id="robot-preview-image"]    ${image_directory}/${order}[Order number].png
#    ${image_file}    Set Variable    ${image_directory}/${order}[Order number].png
#    ${list}    Create List
#    ...    ${image_file}:align=center

#    # Adicionar arquivo de imagem ao PDF
#    Add Files To Pdf
#    ...    ${list}
#    ...    ${output_file}
#    ...    append=True

#    # Fechar o PDF
#    Close Pdf

#    Run Keyword And Ignore Error    Click Button    //*[@id="order-another"]
#    END

# Close the browser
#    Close Browser

To create zip file
    ${zip_file_name}=    Set Variable    ${output_directory}/PDFs.zip
    Archive Folder With Zip    ${pdf_directory}    ${zip_file_name}
