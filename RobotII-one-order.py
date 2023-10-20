from robocorp.tasks import task
from robocorp import browser, http
from RPA.Archive import Archive
from RPA.Desktop import Desktop
from RPA.Tables import Tables
from RPA.PDF import PDF
import time


@task
def order_robots_from_RobotSpareBin():
    """Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file
    Saves the screenshot of the robot to the PDF receipt
    Creates ZIP archive of the receipts and the images"""

    browser.configure(slowmo=200)
    open_the_robot_order_website()
    download_the_csv_file()
    close_annoying_modal()
    fill_one_order_and_submit()
    store_receipt_as_pdf()
    print_robot()
    embed_receipt_and_robot_image()
    order_another_robot()
    create_zip_file()



def open_the_robot_order_website():
    """Navigate to order website"""
    browser.goto('https://robotsparebinindustries.com/#/robot-order')

def download_the_csv_file():
    """Download order csv file"""
    http.download(url="https://robotsparebinindustries.com/orders.csv",
                  overwrite=True)
    
def close_annoying_modal():
    """Click pop up"""
    page = browser.page()
    page.click("text=Yep")


def fill_one_order_and_submit():
    """mask for fill order form and submit it"""
    page = browser.page()
    page.select_option("#head", "Peanut crusher head")
    page.check("#id-body-3")
    page.fill("xpath=//input[@placeholder='Enter the part number for the legs']", "3")
    page.fill("xpath=//input[@placeholder='Shipping address']", 'Clarice Aoto')
    page.click("text=Preview")
    time.sleep(5) 
    page.click("#order")


def store_receipt_as_pdf():
    """Save receipt to pdf file"""
    page = browser.page()
    page.wait_for_selector('#robot-preview-image')
    page.wait_for_selector('#receipt')
    order_receipt = page.locator("#receipt").inner_html()
    pdf = PDF()
    pdf.html_to_pdf(order_receipt, "output/pdf/receipt.pdf")


def print_robot():
    """Take a screenshot and save image"""
    page = browser.page()
    page.screenshot(path="output/img/robot1.png")

    
def embed_receipt_and_robot_image():
    """Embed receipt pdf and page screenshot"""
    pdf = PDF()
    pdf_file = 'output/pdf/receipt.pdf'
    img = "output/img/robot1.png"
    files = [pdf_file, img]
    pdf.add_files_to_pdf(files, 
                         "output/merged.pdf", 
                         append=True)


def order_another_robot():
    """Order another robot"""
    page = browser.page()
    page.click("text=ORDER ANOTHER ROBOT")

def create_zip_file():
    """Create zip file with ordered pdfs"""
    lib = Archive()
    lib.archive_folder_with_zip('output/merged', 'ordered-robots.zip')