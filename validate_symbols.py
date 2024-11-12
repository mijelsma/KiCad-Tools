import os
import sexpdata
from prettytable import PrettyTable
import argparse
from typing import List, Tuple, Union, Dict

# Define the required and optional parameters to check
REQUIRED_FIELDS = ["Reference", "Value", "Footprint", "Description", "Package", "Manufacturer", "Manufacturer Part Number", "Datasheet"]
OPTIONAL_FIELDS = ["ki_keywords", "ki_fp_filters", "ki_description"]

# Define types
Component = List[Union[sexpdata.Symbol, List[Union[sexpdata.Symbol, str]]]]

# Function to extract a property's value and hidden status from the component's S-expression list
def extract_property_and_hidden_status(component: Component, prop_name: str) -> Tuple[Union[str, None], Union[bool, None]]:
    for item in component:
        if isinstance(item, list) and item[0] == sexpdata.Symbol("property") and item[1] == prop_name:
            hidden = False
            for subitem in item:
                if isinstance(subitem, list) and subitem[0] == sexpdata.Symbol("effects"):
                    for effect in subitem:
                        if isinstance(effect, list) and effect[0] == sexpdata.Symbol("hide"):
                            hidden = True
            return item[2], hidden
    return None, None

# Function to check if all required fields are present in the symbol component and if they have the correct hidden status
def check_parameters(component: Component) -> Tuple[List[str], bool, bool]:
    missing_fields: List[str] = []
    extra_fields_exist = False
    correct_visibility = True  # Assume visibility is correct, and flag errors if any

    for field in REQUIRED_FIELDS:
        value, hidden = extract_property_and_hidden_status(component, field)
        if field == "Datasheet" and value is None:
            continue
        if not value:
            missing_fields.append(field)
        else:
            if field in ["Reference", "Value"] and hidden:
                correct_visibility = False
            elif field not in ["Reference", "Value"] and not hidden:
                correct_visibility = False

    all_property_names = [item[1] for item in component if isinstance(item, list) and item[0] == sexpdata.Symbol("property")]

    for field in all_property_names:
        if field not in REQUIRED_FIELDS and field not in OPTIONAL_FIELDS:
            extra_fields_exist = True

    return missing_fields, extra_fields_exist, correct_visibility

# Function to scan all components in a .kicad_sym file
def scan_symbol_file(file_path: str) -> Tuple[List[Tuple[str, List[str], bool, bool]], int, int]:
    issues: List[Tuple[str, List[str], bool, bool]] = []
    total_components = 0
    completed_components = 0
    with open(file_path, 'r') as f:
        content = f.read()
        data = sexpdata.loads(content)
        symbols = [item for item in data if isinstance(item, list) and item[0] == sexpdata.Symbol("symbol")]

        symbols.sort(key=lambda symbol: symbol[1])
        total_components = len(symbols)

        for symbol in symbols:
            symbol_name = symbol[1]
            missing_fields, extra_fields_exist, correct_visibility = check_parameters(symbol)
            if missing_fields or extra_fields_exist or not correct_visibility:
                issues.append((symbol_name, missing_fields, extra_fields_exist, correct_visibility))
            else:
                completed_components += 1

    return issues, completed_components, total_components

# Function to create a pretty table from the scan results
def create_pretty_table(library_name: str, components: List[Tuple[str, List[str], bool, bool]]) -> None:
    table = PrettyTable()
    table.field_names = ["Component Name"] + REQUIRED_FIELDS + ["No Extra Fields", "Correct Visibility"]
    components.sort(key=lambda component: component[0])

    for component, missing_fields, extra_fields_exist, correct_visibility in components:
        row = [component]
        for field in REQUIRED_FIELDS:
            row.append("❌" if field in missing_fields else "✅")
        row.append("✅" if not extra_fields_exist else "❌")
        row.append("✅" if correct_visibility else "❌")
        table.add_row(row)

    print(f"\nResults for library: {library_name}")
    print(table)

# Function to create an overview table for all libraries
def create_overview_table(library_statuses: Dict[str, Tuple[bool, int, int]]) -> None:
    overview_table = PrettyTable()
    overview_table.field_names = ["Library", "Status", "Completed Components"]
    sorted_libraries = sorted(library_statuses.items(), key=lambda x: x[0])

    for library, (status, completed, total) in sorted_libraries:
        overview_table.add_row([library, "✅ Complete" if status else "❌ Needs Work", f"{completed}/{total} components"])

    print("\nOverview of all libraries scanned:")
    print(overview_table)

# Function to scan all .kicad_sym files in the provided directory
def scan_libraries(directory: str) -> None:
    library_statuses: Dict[str, Tuple[bool, int, int]] = {}

    # Get all symbols
    files_to_scan: List[str] = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".kicad_sym"):
                files_to_scan.append(os.path.join(root, file))

    # Sort based on name
    files_to_scan.sort()

    # Scan each symbol library
    for file_path in files_to_scan:
        print(f"Scanning library: {file_path}")
        issues, completed_components, total_components = scan_symbol_file(file_path)
        file_name = os.path.basename(file_path)
        if issues:
            library_statuses[file_name] = (False, completed_components, total_components)
            create_pretty_table(file_name, issues)
        else:
            library_statuses[file_name] = (True, completed_components, total_components)
            print(f"All components in {file_name} have required fields filled, correct visibility, and no extra fields.\n")

    # Make a pretty overview table
    create_overview_table(library_statuses)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scan KiCad symbol libraries for required fields and visibility.")
    parser.add_argument("-p", "--path", type=str, required=True, help="Directory containing the KiCad symbol libraries (.kicad_sym)")

    args = parser.parse_args()
    library_path = args.path

    if not os.path.isdir(library_path):
        print("Error: Provided path is not a directory or does not exist.")
    else:
        scan_libraries(library_path)
