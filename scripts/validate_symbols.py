import os
import sexpdata
from prettytable import PrettyTable
import argparse
from typing import List, Tuple, Union, Dict

REQUIRED_FIELDS = ["Reference", "Value", "Footprint", "Description", "Package", "Manufacturer", "Manufacturer Part Number", "Datasheet"]
OPTIONAL_FIELDS = ["ki_keywords", "ki_fp_filters", "ki_description"]

Component = List[Union[sexpdata.Symbol, List[Union[sexpdata.Symbol, str]]]]


def extract_property_and_hidden_status(component: Component, prop_name: str) -> Tuple[Union[str, None], Union[bool, None]]:
    """Extract a property's value and hidden status from the component's S-expression list."""
    for item in component:
        if isinstance(item, list) and item[0] == sexpdata.Symbol("property") and item[1] == prop_name:
            hidden = any(
                isinstance(subitem, list) and subitem[0] == sexpdata.Symbol("effects") and any(
                    effect[0] == sexpdata.Symbol("hide") for effect in subitem if isinstance(effect, list)
                )
                for subitem in item
            )
            return item[2], hidden
    return None, None


def check_required_fields(component: Component) -> Tuple[List[str], bool]:
    """Check if all required fields are present in the component."""
    missing_fields = [field for field in REQUIRED_FIELDS if not extract_property_and_hidden_status(component, field)[0]]
    extra_fields_exist = any(
        field not in REQUIRED_FIELDS + OPTIONAL_FIELDS for field in [
            item[1] for item in component if isinstance(item, list) and item[0] == sexpdata.Symbol("property")
        ]
    )
    return missing_fields, extra_fields_exist


def check_visibility(component: Component) -> bool:
    """Check if visibility settings for fields are correct."""
    for field in REQUIRED_FIELDS:
        value, hidden = extract_property_and_hidden_status(component, field)
        if field in ["Reference", "Value"] and hidden:
            return False
        elif field not in ["Reference", "Value"] and not hidden:
            return False
    return True


def check_component(component: Component) -> Tuple[str, List[str], bool, bool]:
    """Check a single component for missing fields, extra fields, and correct visibility."""
    component_name = component[1]
    missing_fields, extra_fields_exist = check_required_fields(component)
    correct_visibility = check_visibility(component)
    return component_name, missing_fields, extra_fields_exist, correct_visibility


def scan_symbol_file(file_path: str) -> Tuple[List[Tuple[str, List[str], bool, bool]], int, int]:
    """Scan a .kicad_sym file for component issues."""
    issues = []
    with open(file_path, 'r') as f:
        symbols = [item for item in sexpdata.loads(f.read()) if isinstance(item, list) and item[0] == sexpdata.Symbol("symbol")]

    for symbol in symbols:
        component_name, missing_fields, extra_fields_exist, correct_visibility = check_component(symbol)
        if missing_fields or extra_fields_exist or not correct_visibility:
            issues.append((component_name, missing_fields, extra_fields_exist, correct_visibility))

    return issues, len(symbols) - len(issues), len(symbols)


def create_pretty_table(library_name: str, components: List[Tuple[str, List[str], bool, bool]]) -> None:
    """Create and print a detailed table of the scan results for a library."""
    table = PrettyTable()
    table.field_names = ["Component Name"] + REQUIRED_FIELDS + ["No Extra Fields", "Correct Visibility"]

    for component_name, missing_fields, extra_fields_exist, correct_visibility in components:
        row = [component_name] + ["❌" if field in missing_fields else "✅" for field in REQUIRED_FIELDS]
        row += ["✅" if not extra_fields_exist else "❌", "✅" if correct_visibility else "❌"]
        table.add_row(row)

    print(f"\nResults for library: {library_name}")
    print(table)


def create_overview_table(library_statuses: Dict[str, Tuple[bool, int, int]]) -> None:
    """Create and print an overview table for all libraries."""
    overview_table = PrettyTable()
    overview_table.field_names = ["Library", "Status", "Completed Components"]

    for library, (status, completed, total) in sorted(library_statuses.items()):
        overview_table.add_row([library, "✅ Complete" if status else "❌ Needs Work", f"{completed}/{total} components"])

    print("\nOverview of all libraries scanned:")
    print(overview_table)


def scan_libraries(directory: str) -> None:
    """Scan all .kicad_sym files in a directory."""
    library_statuses = {}
    for root, _, files in os.walk(directory):
        for file in sorted(files):
            if file.endswith(".kicad_sym"):
                file_path = os.path.join(root, file)
                print(f"Scanning library: {file_path}")
                issues, completed, total = scan_symbol_file(file_path)
                if issues:
                    library_statuses[file] = (False, completed, total)
                    create_pretty_table(file, issues)
                else:
                    library_statuses[file] = (True, completed, total)
                    print(f"All components in {file} have required fields filled, correct visibility, and no extra fields.\n")

    create_overview_table(library_statuses)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scan KiCad symbol libraries for required fields and visibility.")
    parser.add_argument("-p", "--path", type=str, required=True, help="Directory containing the KiCad symbol libraries (.kicad_sym)")
    args = parser.parse_args()

    if os.path.isdir(args.path):
        scan_libraries(args.path)
    else:
        print("Error: Provided path is not a directory or does not exist.")
