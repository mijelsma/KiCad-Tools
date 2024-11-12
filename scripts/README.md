# KiCad Scripts

## Overview

This directory contains Python scripts designed to automate and simplify repetitive or 'tedious' tasks often encountered in KiCad projects. These tools help streamline project setup and ensure consistency in component specifications, reducing time spent on manual tasks and minimizing potential errors.

## Features

- **Project Creation**: Quickly create a new KiCad project with a standardized directory structure and basic README.
- **Symbol Library Validation**: Ensure all symbols meet specified standards, with checks for required component information.

---

### Create a New Project

To create a new KiCad project, run the following command, replacing `YOUR_PROJECT_NAME` with your desired project name:

```bash
python create_project.py --name YOUR_PROJECT_NAME
```

This command creates a new KiCad project based on the `TEMPLATE_PROJECT` folder. It will:

Copy the recommended project structure,
Rename all files appropriately,
Generate an empty `README.md` for documentation.


### Validate Symbol Library
Accurate component specifications are essential for successful PCB assembly. The `validate_symbols.py `script checks that each symbol in the KiCad library has the following key parameters defined, which are typically required by assembly services:

- **Value**: A visible identifier on the schematic, like 10k or a part number.
- **Package**: The component's footprint.
- **Manufacturer**: The name of the component’s manufacturer.
- **Manufacturer Part Number**: The specific part number assigned by the manufacturer.

Additionally, the script verifies that each component has a defined footprint and that visibility settings for parameters are properly configured. These settings are based on personal preferences but can be customized within the script.

Run the script with:

```bash
python validate_symbols.py --project /path/to/your/project
```

