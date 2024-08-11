# Subsurface Visualization Tool

## Created by: Heba Alazzeh

### Overview
This tool is designed to load, process, and visualize 3D subsurface data from multiple anisotropic and isotropic CSV files. The tool allows users to toggle between different visualization modes: standard view, interactive slicing, and structure identification.

### Features
- **Standard View**: Displays the full 3D volumetric data.
- **Interactive Slicing**: Allows users to slice through the 3D data along the x, y, and z axes interactively.
- **Structure Identification**: Isolates and visualizes specific structures, such as ore bodies, based on threshold values.

### Requirements
- Python 3.6+
- Required Python packages:
  - `pandas`
  - `numpy`
  - `mayavi`
  - `traits`
  - `traitsui`

### Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/subsurface-visualization-tool.git
   cd subsurface-visualization-tool
