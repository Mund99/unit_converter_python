import datetime
import os
import csv
from tabulate import tabulate

# Default history file location
HISTORY_FILE = "conversion_history.txt"

def log_conversion(category, from_unit, to_unit, value, result, history_file=None):
    """Log a conversion to the history file with error handling."""
    try:
        # Use the provided history file or the default
        file_to_use = history_file if history_file else HISTORY_FILE

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} | {category} | {from_unit} | {to_unit} | {value} | {result}\n"
        with open(file_to_use, "a") as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Warning: Could not log conversion: {e}")

def show_history(history_file=None, limit=None, category_filter=None):
    """
    Display the conversion history in a formatted table.

    Args:
        history_file: Optional custom history file path
        limit: Optional limit on number of entries to show (most recent first)
        category_filter: Optional category to filter by (e.g., "Length", "Temperature")
    """
    try:
        # Use the provided history file or the default
        file_to_use = history_file if history_file else HISTORY_FILE

        if not os.path.exists(file_to_use) or os.path.getsize(file_to_use) == 0:
            print("No conversion history found.")
            return

        # Read history data into a list of lists
        history_data = []
        with open(file_to_use, "r") as f:
            for line in f:
                parts = line.strip().split(" | ")
                if len(parts) == 6:  # Ensure we have all expected parts
                    # Apply category filter if specified
                    if category_filter and parts[1].lower() != category_filter.lower():
                        continue
                    history_data.append(parts)

        # Sort by timestamp (newest first)
        history_data.sort(key=lambda x: x[0], reverse=True)

        # Apply limit if specified
        if limit and limit > 0 and limit < len(history_data):
            history_data = history_data[:limit]
            print(f"\n=== Conversion History (Latest {limit} Entries) ===")
        else:
            print("\n=== Conversion History ===")

        if category_filter:
            print(f"Filtered by category: {category_filter}")

        # Display using tabulate
        print(tabulate(history_data,
                      headers=["Timestamp", "Category", "From", "To", "Input Value", "Result"],
                      tablefmt="pretty"))
    except Exception as e:
        print(f"Error accessing history file: {e}")

def clear_history(history_file=None, confirm=True):
    """Clear the conversion history with error handling and confirmation."""
    try:
        # Use the provided history file or the default
        file_to_use = history_file if history_file else HISTORY_FILE

        if not os.path.exists(file_to_use):
            print("No history file exists yet.")
            return

        if confirm:
            confirmation = input("Are you sure you want to clear the conversion history? (y/n): ").lower()
            if confirmation != 'y' and confirmation != 'yes':
                print("Operation cancelled.")
                return

        open(file_to_use, "w").close()
        print("Conversion history cleared.")
    except Exception as e:
        print(f"Error clearing history: {e}")

def export_history_to_csv(csv_filename, history_file=None):
    """Export conversion history to a CSV file."""
    try:
        # Use the provided history file or the default
        file_to_use = history_file if history_file else HISTORY_FILE

        if not os.path.exists(file_to_use) or os.path.getsize(file_to_use) == 0:
            print("No conversion history found to export.")
            return False

        with open(file_to_use, "r") as history_file, open(csv_filename, "w", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            # Write header
            csv_writer.writerow(["Timestamp", "Category", "From Unit", "To Unit", "Input Value", "Result"])

            # Write data
            for line in history_file:
                parts = line.strip().split(" | ")
                if len(parts) == 6:  # Ensure we have all expected parts
                    csv_writer.writerow(parts)

        print(f"Conversion history exported to {csv_filename}")
        return True
    except Exception as e:
        print(f"Error exporting history to CSV: {e}")
        return False

# Length conversion constants
LENGTH_UNITS = {
    "meters": 1.0,
    "feet": 3.28084,
    "inches": 39.3701,
    "centimeters": 100.0,
    "kilometers": 0.001,
    "miles": 0.000621371
}

# Volume conversion constants
VOLUME_UNITS = {
    "liters": 1.0,
    "milliliters": 1000.0,
    "gallons": 0.264172,
    "cups": 4.22675,
    "cubic meters": 0.001
}

# Temperature conversion functions
def celsius_to_fahrenheit(c):
    return (c * 9/5) + 32

def fahrenheit_to_celsius(f):
    return (f - 32) * 5/9

def celsius_to_kelvin(c):
    return c + 273.15

def kelvin_to_celsius(k):
    return k - 273.15

def fahrenheit_to_kelvin(f):
    return (f - 32) * 5/9 + 273.15

def kelvin_to_fahrenheit(k):
    return (k - 273.15) * 9/5 + 32

# Weight conversion constants
WEIGHT_UNITS = {
    "kilograms": 1.0,
    "grams": 1000.0,
    "pounds": 2.20462,
    "ounces": 35.274
}

def generic_conversion(category, units_dict, base_unit_name, history_file=None):
    """Generic conversion function for units that use a simple conversion factor."""
    print(f"\n=== {category} Conversion ===")
    print("Available units:")
    for i, unit in enumerate(units_dict.keys(), 1):
        print(f"{i}. {unit}")

    max_choice = len(units_dict)

    try:
        from_choice = int(input(f"Select 'from' unit (1-{max_choice}): "))
        to_choice = int(input(f"Select 'to' unit (1-{max_choice}): "))
        value = float(input("Enter value to convert: "))

        if 1 <= from_choice <= max_choice and 1 <= to_choice <= max_choice:
            from_unit = list(units_dict.keys())[from_choice - 1]
            to_unit = list(units_dict.keys())[to_choice - 1]

            # Convert to base unit first, then to target unit
            base_value = value / units_dict[from_unit]
            result = base_value * units_dict[to_unit]

            # Format the result using tabulate
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            result_table = [[timestamp, category, from_unit, to_unit, value, f"{result:.4f}"]]
            print("\n=== Conversion Result ===")
            print(tabulate(result_table,
                          headers=["Timestamp", "Category", "From", "To", "Input Value", "Result"],
                          tablefmt="pretty"))

            log_conversion(category, from_unit, to_unit, value, result, history_file)
        else:
            print("Invalid unit selection.")
    except ValueError:
        print("Invalid input. Please enter numbers only.")
    except Exception as e:
        print(f"An error occurred: {e}")

def weight_conversion(history_file=None):
    generic_conversion("Weight", WEIGHT_UNITS, "kilograms", history_file)

def volume_conversion(history_file=None):
    generic_conversion("Volume", VOLUME_UNITS, "liters", history_file)

def length_conversion(history_file=None):
    generic_conversion("Length", LENGTH_UNITS, "meters", history_file)

def temperature_conversion(history_file=None):
    print("\n=== Temperature Conversion ===")
    print("Available units:")
    print("1. Celsius")
    print("2. Fahrenheit")
    print("3. Kelvin")

    try:
        from_choice = int(input("Select 'from' unit (1-3): "))
        to_choice = int(input("Select 'to' unit (1-3): "))
        value = float(input("Enter temperature to convert: "))

        if 1 <= from_choice <= 3 and 1 <= to_choice <= 3:
            units = ["Celsius", "Fahrenheit", "Kelvin"]
            from_unit = units[from_choice - 1]
            to_unit = units[to_choice - 1]

            # Convert to Celsius first
            if from_unit == "Celsius":
                celsius = value
            elif from_unit == "Fahrenheit":
                celsius = fahrenheit_to_celsius(value)
            else:  # Kelvin
                celsius = kelvin_to_celsius(value)

            # Convert from Celsius to target unit
            if to_unit == "Celsius":
                result = celsius
            elif to_unit == "Fahrenheit":
                result = celsius_to_fahrenheit(celsius)
            else:  # Kelvin
                result = celsius_to_kelvin(celsius)

            # Format the result using tabulate
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            result_table = [[timestamp, "Temperature", from_unit, to_unit, value, f"{result:.4f}"]]
            print("\n=== Conversion Result ===")
            print(tabulate(result_table,
                          headers=["Timestamp", "Category", "From", "To", "Input Value", "Result"],
                          tablefmt="pretty"))

            log_conversion("Temperature", from_unit, to_unit, value, result, history_file)
        else:
            print("Invalid unit selection.")
    except ValueError:
        print("Invalid input. Please enter numbers only.")
    except Exception as e:
        print(f"An error occurred: {e}")

def history_menu():
    """Sub-menu for history-related operations."""
    while True:
        print("\n=== History Options ===")
        print("1. View All History")
        print("2. View Limited History")
        print("3. Filter History by Category")
        print("4. Clear History")
        print("5. Export History to CSV")
        print("6. Return to Main Menu")

        choice = input("Select an option (1-6): ")

        if choice == "1":
            show_history()
        elif choice == "2":
            try:
                limit = int(input("Enter number of entries to show: "))
                show_history(limit=limit)
            except ValueError:
                print("Invalid input. Please enter a number.")
        elif choice == "3":
            print("Available categories:")
            print("1. Length")
            print("2. Volume")
            print("3. Temperature")
            print("4. Weight")
            cat_choice = input("Select category (1-4): ")

            categories = {
                "1": "Length",
                "2": "Volume",
                "3": "Temperature",
                "4": "Weight"
            }

            if cat_choice in categories:
                show_history(category_filter=categories[cat_choice])
            else:
                print("Invalid category selection.")
        elif choice == "4":
            clear_history()
        elif choice == "5":
            filename = input("Enter CSV filename to export to: ")
            if filename:
                # Check if the filename already has .csv extension
                if not filename.lower().endswith('.csv'):
                    filename += '.csv'
                export_history_to_csv(filename)
            else:
                print("Export cancelled.")
        elif choice == "6":
            return
        else:
            print("Invalid choice. Please try again.")

def main_menu():
    while True:
        print("\n=== Unit Converter ===")
        print("1. Length")
        print("2. Volume")
        print("3. Temperature")
        print("4. Weight")
        print("5. History Options")
        print("6. Exit")

        choice = input("Select an option (1-6): ")

        if choice == "1":
            length_conversion()
        elif choice == "2":
            volume_conversion()
        elif choice == "3":
            temperature_conversion()
        elif choice == "4":
            weight_conversion()
        elif choice == "5":
            history_menu()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
