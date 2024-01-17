import pandas as pd
import qrcode
import time
import logging
from bs4 import BeautifulSoup
from qrcode.image.svg import SvgPathImage
from xml.etree import ElementTree

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Sample base URL - replace with your actual base URL
base_url = "http://eschoolapp.in/sample-reports?crmid="

# Function to generate SVG QR code images
def generate_qr_code_svg(url, method='path'):
    logging.info(f"Generating QR code for URL: {url}")
    if method == 'basic':
        factory = qrcode.image.svg.SvgImage
    elif method == 'fragment':
        factory = qrcode.image.svg.SvgFragmentImage
    else:  # 'path' or any other value
        factory = qrcode.image.svg.SvgPathImage

    qr = qrcode.QRCode(
        version=1,  # Adjust as needed to fit your data
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,  # Adjust based on your desired size
        border=4,     # Border in boxes, not pixels
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(image_factory=factory)

    # Convert the SVG image object to a string
    img_buffer = ElementTree.tostring(img._img, encoding='unicode', method='xml')
    logging.info("QR code generated successfully.")
    return img_buffer

# Read CSV file
path = 'deta.csv'
df = pd.read_csv(path)

# Start measuring time
start_time = time.time()

# Load the HTML template
with open("index.html", "r") as template_file:
    logging.info("Loading HTML template.")
    template = template_file.read()

# Initialize a variable to hold the combined HTML content
combined_html = ""
# Iterate through each row in the CSV
for index, row in df.iterrows():
    soup = BeautifulSoup(template, 'html.parser')

    url = base_url + str(row['ID'])
    qr_code_svg = generate_qr_code_svg(url)

    lawyer_name = row['Lawyer Name']

    # Replace placeholders
    logging.info(f"Replacing placeholders for record {index + 1}.")
    for td in soup.find_all('td'):
        if '{qr_code}' in str(td):
            td.clear()
            td.append(BeautifulSoup(qr_code_svg, 'html.parser'))
        elif '{lawyer_name}' in str(td):
            td.clear()
            td.append(lawyer_name)
            additional_text = """
            <p class="mort" style="color: #3a3401; font-weight: normal; font-style: normal; font-size: 12px;">Scan me to View Sample Reports</p>
            <p class="mort" style="color: #3a3401; font-weight: normal; font-style: normal; font-size: 12px;">Link: eschoolapp.in/sample</p>
            """
            td.append(BeautifulSoup(additional_text, 'html.parser'))

    combined_html += str(soup)

# # Iterate through each row in the CSV
# for index, row in df.iterrows():

#         soup = BeautifulSoup(template, 'html.parser')

#         url = base_url + str(row['ID'])
#         qr_code_svg = generate_qr_code_svg(url)

#         lawyer_name = row['Lawyer Name']
#         additional_text = ""
#         # Replace placeholders
#         logging.info(f"Replacing placeholders for record {index + 1}.")
#         for td in soup.find_all('td'):
#             if '{qr_code}' in str(td):
#                 td.clear()
#                 td.append(BeautifulSoup(qr_code_svg, 'html.parser'))
#             elif '{lawyer_name}' in str(td):
#                 td.clear()
#                 td.append(lawyer_name)
#                 additional_text = """
#             <p class="mort"style="color: #3a3401; font-weight: normal; font-style: normal;font-size: 12px;">Scan me to View Sample Reports</p>
#             <p class="mort"style="color: #3a3401; font-weight: normal; font-style: normal;font-size: 12px;">Link: eschoolapp.in/sample</p>
#             """
#             td.append(BeautifulSoup(additional_text, 'html.parser'))

#         combined_html += str(soup)
        

# Write the combined HTML to a single output file
with open("combined_output.html", "w") as output_file:
    logging.info("Writing combined HTML to file.")
    output_file.write(combined_html)

import pdfkit

options = {
    'javascript-delay': 1000,  # Wait for 1000 milliseconds (1 second)
    'enable-local-file-access': True  # Allow access to local files
}

# Convert HTML to PDF
try:
    pdfkit.from_file('combined_output.html', 'combined_output.pdf', options=options)
    print("PDF created successfully.")
except Exception as e:
    print(f"Error during PDF creation: {e}")

# Measure end time and log completion

end_time = time.time()
time_taken = end_time - start_time
print(f"Total time taken: {time_taken} seconds")
logging.info(f"Consolidated HTML file with QR codes generated. Total time taken: {time_taken} seconds")