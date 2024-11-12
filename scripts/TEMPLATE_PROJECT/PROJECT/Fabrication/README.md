# Fabrication

## Overview

This directory contains all the files and information necessary for fabricating and assembling the PCB, including:

- **BOM**: The Bill of Materials (`BOM`) file listing all components required for the project.
- **CPL**: The Component Placement List (`CPL`) file specifying component positions on the PCB.
- **Gerber**: The Gerber files, which contain the design data required by PCB manufacturers to create the physical board.
- **PCB-Manufacturing-Info.txt**: A file detailing the specifications and requirements for PCB manufacturing, such as board thickness, layer stackup, and soldermask color.

Each subdirectory and file has its specific purpose and is documented in its own `README.md` for more details.

### Key Files

- **BOM**: `BOM.csv` - Contains details about each component for procurement.
- **CPL**: `CPL.csv` - Provides data on component placement for assembly.
- **Gerber**: Files needed to manufacture the PCB (see the `Gerber` directory for details).
- **PCB-Manufacturing-Info.txt**: Contains essential specifications for the PCB, including:

  - **Board Thickness**: The overall thickness of the PCB
  - **Dimensions**: Physical dimensions of the board
  - **Number of Layers**: The layer count for the board
  - **Minimum Track Width**: The smallest allowable track width
  - **Minimum Spacing**: The minimum distance between tracks or components
  - **Minimum Hole Size**: The smallest allowable hole size
  - **Soldermask Color**: Color of the soldermask (e.g., green, black)
  - **Silkscreen Color**: Color of the silkscreen for labeling (e.g., white, black)
  - **Special Requirements**: Any additional specific requirements for manufacturing
  - **Layer Stackup**: A description of each layer, its purpose, and thickness

This information ensures that the PCB is fabricated to meet design and performance requirements.
