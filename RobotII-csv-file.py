from robocorp.tasks import task
from robocorp import browser, http

from RPA.Tables import Tables
from RPA.PDF import PDF
import time
from RPA.Archive import Archive



@task
def order_robots_from_RobotSpareBin():
    """Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file
    Saves the screenshot of the robot to the PDF receipt
    Creates ZIP archive of the receipts and the images"""

    browser.configure(slowmo=100)
    open_the_robot_order_website()
    download_the_csv_file()
    loop_orders()




def open_the_robot_order_website():
    """Navigate to order website"""
    browser.goto('https://robotsparebinindustries.com/#/robot-order')

def download_the_csv_file():
    """Download order csv file"""
    http.download(url="https://robotsparebinindustries.com/orders.csv",
                  overwrite=True)
    
def loop_orders():
    """loop to order robot"""
    close_annoying_modal()
    fill_orders_from_csv_file()
    order_another_robot()
    create_zip_file()

#Subtasks

def close_annoying_modal():
    """Click pop up"""
    page = browser.page()
    page.click("text=Yep")

def fill_orders_from_csv_file():
    """open the csv file and use fill_one_order_and_submit function to get all orders"""
    library = Tables()
    orders = library.read_table_from_csv("orders.csv",
                                         header = True,
                                         columns = ['Order number', 'Head', 'Body', 'Legs', 'Address']
                                         )
    for row in orders:
        fill_one_order_and_submit(row=row, order_number=row)
        store_receipt_as_pdf(order_number=row)
        print_robot(order_number=row)
        embed_receipt_and_robot_image(order_number=row)


def fill_one_order_and_submit(row, order_number):
    """mask for fill order form and submit it"""
    page = browser.page()
    page.select_option("#head", row['Head'])
    page.check(f"#id-body-{str(row['Body'])}")
    page.fill("xpath=//input[@placeholder='Enter the part number for the legs']", 
              str(row['Legs']))
    page.fill("xpath=//input[@placeholder='Shipping address']", 
              str(row['Address']))
    page.click("text=Preview")
    page.wait_for_selector('#order')
    page.click("text=Order")
    
def store_receipt_as_pdf(order_number):
    """Store the order receipt as a PDF file"""
    page = browser.page()  
    time.sleep(3)
    page.wait_for_selector('#robot-preview-image')
    page.wait_for_selector('#receipt')  
    receipt = page.locator("#receipt").inner_html()
    pdf = PDF()
    pdf.html_to_pdf(receipt, 
                    f"output/pdf/{order_number['Order number']}.pdf")

def print_robot(order_number):
    """take page screenshot"""
    page = browser.page()
    page.screenshot(path=f"output/img/{order_number['Order number']}.png")

def embed_receipt_and_robot_image(order_number):
    """merge receipt pdf and page screenshot"""
    pdf = PDF()
    pdf_file = f"output/{order_number['Order number']}.pdf"
    img = f"output/img/{order_number['Order number']}.png"
    files = [pdf_file, img]
    pdf.add_files_to_pdf(files, 
                         f"output/merged/{order_number['Order number']}.pdf", 
                         append=False)
        
def order_another_robot():
    """Order another robot"""
    page = browser.page()
    page.click("text=ORDER ANOTHER ROBOT")

def create_zip_file():
    """Create zip file with ordered pdfs"""
    lib = Archive()
    lib.archive_folder_with_zip('output/merged', 'ordered-robots.zip')