# Bulk QR Code Generator

This Python script generates QR codes in bulk from a CSV file, embeds them into an HTML file, and applies custom styling. It's designed for efficient creation and display of QR codes, making it ideal for generating large numbers of QR codes for various applications.

## Features

- Generates QR codes from URLs provided in a CSV file.
- Option to embed a logo within each QR code.
- Outputs an HTML file displaying the QR codes with additional styling and text.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

- Python 3.x
- Pip (Python package installer)

### Installing

First, clone the repository to your local machine:

git clone https://github.com/your-username/StickyGoo.git

Navigate to the project directory:

cd StickyGoo

Install the required Python packages:

pip install -r reqirements.txt

Usage

    Place your CSV file in the project directory. This file should contain the data required for QR code generation.
    Update the path variable in the script to match the name of your CSV file.
    Run the script:

python main.py

After running the script, you'll find an HTML file named qr_codes.html in your project directory, containing the generated QR codes.
Configuration

    Modify base_url in the script to change the base URL used for generating QR codes.
    Update logo_path in the script with the path to your logo image if you wish to embed a logo in each QR code.

Contributing

Contributions are welcome, and any feedback or suggestions are appreciated. Feel free to fork the project and submit pull requests. You can also open an issue for bugs, feature requests, or any other queries.
