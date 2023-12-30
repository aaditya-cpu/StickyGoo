import pandas as pd
import qrcode
from io import BytesIO
import base64
import time
import logging
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
from qrcode.image.styledpil import StyledPilImage

# Setup basic logging
logging.basicConfig(level=logging.INFO)

# Sample base URL - replace with your actual base URL
base_url = "http://eschoolapp.in/sample-reports?crmid="

# Function to generate QR code images as base64 encoded strings
def generate_qr_code(url, logo_path):
    qr = qrcode.QRCode(
        version=1,  # Adjust as needed to fit your data
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=6,  # Adjust based on trial and error for size
        border=1,    # Border in boxes, not pixels
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Set the colors
    fill_color = (41, 72, 85)  # Dark blue color in RGB
    back_color = (255, 255, 255)  # White background in RGB

    img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(),
        color_mask=SolidFillColorMask(back_color=back_color, front_color=fill_color),
        # embeded_image_path=logo_path
    )
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Read CSV file
path = 'deta.csv'  
df = pd.read_csv(path)

# Specify the path to the logo image
logo_path = 'log.png' 

# Start measuring time
start_time = time.time()

# Generate URLs and QR codes
for index, row in df.iterrows():
    url = base_url + str(row['ID'])
    df.at[index, 'URL'] = url
    qr_code = generate_qr_code(url, logo_path)
    df.at[index, 'QR Code'] = qr_code
    logging.info(f"QR code generated for ID: {row['ID']}")

# Save updated DataFrame back to CSV
df.to_csv(path, index=False)
logging.info("CSV file updated with URLs and QR codes.")

# Measure end time
end_time = time.time()
time_taken = end_time - start_time
logging.info(f"Total time taken: {time_taken} seconds")

# Start HTML string with styles
html_content = """<html><head><style>
table { width: 100%; border-collapse: collapse; }
td { width: 25%; text-align: center; border: 1px solid black; aspect-ratio: 1 / 1; }
.qr-code-img { max-width: 80%; max-height: 80%; }
.lawyer-name { color: #cccccc; background-color: #294855; font-family: 'Droid Sans Mono', 'monospace', monospace; font-weight: 600; font-size: 14px; line-height: 19px; text-align:middle;}
.lawyer-name span { color: #ffffff; }
</style></head><body><table>"""

# Add QR codes, Lawyer Names, and accompanying text to HTML
for i in range(0, len(df), 4):
    html_content += "<tr>"
    for j in range(4):
        if i + j < len(df):
            qr_code = df.iloc[i + j]['QR Code']
            lawyer_name = df.iloc[i + j]['Lawyer Name']
            html_content += f'<td><img class="qr-code-img" src="data:image/png;base64,{qr_code}" alt="QR Code"/><div class="lawyer-name"><span>{lawyer_name}</span></div><p><strong style="text-transform:uppercase;">Scan me</strong> to know more about our comprehensive reports</p></td>'
        else:
            html_content += '<td></td>'
    html_content += "</tr>"

html_content += "</table></body></html>"

# Save HTML to file
with open("qr_codes.html", "w") as file:
    file.write(html_content)
logging.info("HTML file with QR codes generated.")

print(f"Total time taken: {time_taken} seconds")
