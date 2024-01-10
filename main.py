import pandas as pd
import qrcode
from io import BytesIO
import base64  
import time
import logging
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.svg import SvgImage
import xml.etree.ElementTree as ET 

from bs4 import BeautifulSoup
# Setup basic logging# Setup basic logging
logging.basicConfig(level=logging.INFO)

# Sample base URL - replace with your actual base URL
base_url = "http://eschoolapp.in/sample-reports?crmid="

# Function to generate SVG QR code images as text
def generate_qr_code_svg(url):
    qr = qrcode.QRCode(
        version=1,  # Adjust as needed to fit your data
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,  # Adjust based on your desired size
        border=4,    # Border in boxes, not pixels
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Create an SvgImage with a white background
    img = qr.make_image(image_factory=SvgImage, module_drawer=None, background="#FFFFFF")

    # Get the SVG code as text
    svg_text = ET.tostring(img.get_image(), encoding="unicode")
    return svg_text

# Read CSV file
path = 'deta.csv'
df = pd.read_csv(path)

# Start measuring time
start_time = time.time()

# Load the HTML template
with open("index.html", "r") as template_file:
    template_content = template_file.read()

# Create a BeautifulSoup object to parse the template
soup = BeautifulSoup(template_content, 'html.parser')

# Find the table where you want to add QR codes and lawyer names
table = soup.find('table')

# Create a new HTML file for output
with open("qrcode.html", "w") as output_file:
    # Iterate through each row in the CSV
    for index, row in df.iterrows():
        url = base_url + str(row['ID'])
        qr_code_svg = generate_qr_code_svg(url)
        lawyer_name = row['Lawyer Name']

        # Clone the entire template for each row
        row_template = BeautifulSoup(str(table), 'html.parser')

        # Replace the placeholders with the SVG QR code and lawyer name
        placeholders = row_template.find_all(string=True)
        for placeholder in placeholders:
            if "{qr_code}" in placeholder:
                placeholder.replace_with(qr_code_svg)
            elif "{lawyer_name}" in placeholder:
                placeholder.replace_with(lawyer_name)

        # Append the modified row_template to the main table
        table.append(row_template)

        # Log progress for each row
        logging.info(f"Processed row {index + 1} - Lawyer Name: {lawyer_name}, QR Code URL: {url}")

        # Save the modified HTML to the output file after processing each row
        output_file.write(str(soup))

# Log completion
logging.info("HTML file with SVG QR codes generated.")

# Measure end time
end_time = time.time()
time_taken = end_time - start_time
logging.info(f"Total time taken: {time_taken} seconds")

print(f"Total time taken: {time_taken} seconds")