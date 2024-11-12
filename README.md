# KiCad Tools

## Overview

**KiCad Tools** is a collection of Python scripts and utilities designed to streamline the setup, validation, and management of new KiCad projects. These tools help automate tasks, enforce consistency, and ensure that common checks are performed throughout the design process, saving time and reducing errors in PCB development.

## Features

- **Quick Project Setup**: Initialize a new KiCad project structure with commonly used directories, templates, and files.

- **Library Symbol Validation**: Automatically checks component symbols to ensure they meet standard conventions, helping maintain consistency and quality. Provide warnings for common issues, such as missing footprints or incorrect symbol attributes, before they become major problems.

- **BOM and CPL Generation**: Scripts for generating and formatting Bill of Materials (BOM) and Component Placement List (CPL) files, with options for custom formatting. (TODO)

- **3D Rendering Support**: Tools to generate and manage 3D views of the project, ensuring a clear visual reference for the design. (TODO)

- **Fabrication File Management**: Utilities for generating and organizing fabrication files, including Gerber and drill files, to streamline the production handoff.

## Getting Started

### Prerequisites

- **Python 3.x**: Ensure Python is installed on your system.
- **KiCad**: KiCad 8.x or later is recommended for compatibility with all scripts.
- **Required Libraries**: Some Python packages may be needed for specific tools (e.g., `pandas` for BOM generation). Install dependencies using:

  ```bash
  pip install -r requirements.txt
  ```
  
### Installation
Clone this repository to your local machine:

```bash
git clone https://github.com/mijelsma/KiCad-Tools
cd kicad-tools
```

### Usage
Each tool in this repository is designed for a specific task. You can find detailed usage instructions and examples in the `docs/` folder or in each script’s docstring.

For example, to validate symbols in your project library:

```bash
python validate_symbols.py --project /path/to/your/project
```

## Directory Structure
`/scripts`: Contains individual Python scripts for different tasks (e.g., symbol validation, BOM generation).
