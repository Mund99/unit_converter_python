# Unit Converter Python CLI

A command-line unit converter program that supports conversions between different units of measurement.

## Features

- Convert between units in four categories:
  - Length: meters, feet, inches, centimeters, kilometers, miles
  - Volume: liters, milliliters, gallons, cups, cubic meters
  - Temperature: Celsius, Fahrenheit, Kelvin
  - Weight: kilograms, grams, pounds, ounces
- View conversion history in a formatted table
- Filter history by category
- Limit history display to a specific number of entries
- Clear conversion history (with confirmation)
- Export conversion history to CSV
- Case-insensitive unit handling
- Tabular display of conversion results
- Simple and intuitive interface

## Usage

### Interactive Mode

1. Clone the repository
   ```
   git clone https://github.com/Mund99/unit_converter_python
   ```
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the program:
   ```bash
   python unit_converter.py
   ```
4. Follow the on-screen instructions

#### Main Menu Options
- Length Conversion
- Volume Conversion
- Temperature Conversion
- Weight Conversion
- History Options (submenu)
- Exit

#### History Submenu Options
- View All History
- View Limited History
- Filter History by Category
- Clear History
- Export History to CSV
- Return to Main Menu

## Requirements

- Python 3.x
- tabulate==0.9.0
