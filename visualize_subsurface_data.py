"""
Subsurface Visualization Tool
Created by: Heba Alazzeh
Function: This script loads, processes, and visualizes 3D subsurface data from multiple anisotropic and isotropic CSV files. 
          The data is visualized using interactive 3D volumetric plots with color representing field values.
Last Updated: 08/10/2024
"""

import pandas as pd
import numpy as np
from mayavi import mlab

# List of file paths for anisotropic and isotropic data
anisotropic_files = [
    'plot_data_anisotropic_1.csv',
    'plot_data_anisotropic_2.csv',
    'plot_data_anisotropic_3.csv',
    'plot_data_anisotropic_4.csv',
    'plot_data_anisotropic_5.csv',
    'plot_data_anisotropic_6.csv'
]

isotropic_files = [
    'plot_data_isotropic_1.csv',
    'plot_data_isotropic_2.csv',
    'plot_data_isotropic_3.csv',
    'plot_data_isotropic_4.csv',
    'plot_data_isotropic_5.csv',
    'plot_data_isotropic_6.csv'
]

# Function to load and combine CSV files


def load_and_combine(files):
    combined_data = pd.concat([pd.read_csv(file)
                              for file in files], ignore_index=True)
    return combined_data


# Load and combine the data
anisotropic_data = load_and_combine(anisotropic_files)
isotropic_data = load_and_combine(isotropic_files)

# Aggregate the values by taking the mean for each (x, y, z) coordinate


def aggregate_data(data):
    aggregated_data = data.groupby(['x', 'y', 'z'], as_index=False).mean()
    return aggregated_data


anisotropic_data = aggregate_data(anisotropic_data)
isotropic_data = aggregate_data(isotropic_data)

# Extract unique coordinates and reshape the data


def reshape_data(data):
    x_unique = np.unique(data['x'])
    y_unique = np.unique(data['y'])
    z_unique = np.unique(data['z'])

    x_count = len(x_unique)
    y_count = len(y_unique)
    z_count = len(z_unique)

    value_3d = data['value'].values.reshape((x_count, y_count, z_count))
    return x_unique, y_unique, z_unique, value_3d


x_unique_a, y_unique_a, z_unique_a, value_3d_a = reshape_data(anisotropic_data)
x_unique_i, y_unique_i, z_unique_i, value_3d_i = reshape_data(isotropic_data)

# Function to plot 3D volumetric data using mayavi


def plot_3d_volume(x, y, z, data, title, cmap='viridis'):
    # Create meshgrid
    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')

    # Create the figure with a larger size for better resolution
    mlab.figure(title, bgcolor=(1, 1, 1), size=(1200, 900))

    # Create a scalar field
    src = mlab.pipeline.scalar_field(X, Y, Z, data)

    # Visualize the scalar field
    vol = mlab.pipeline.volume(src, vmin=data.min(), vmax=data.max())

    # Adjust the opacity transfer function
    vol._volume_property.scalar_opacity_unit_distance = 0.5
    vol.update_pipeline()

    # Add axes and title with better visibility
    mlab.axes(color=(0, 0, 0))  # Black color for the axes text
    # Black color for the title text
    mlab.title(title, size=0.5, color=(0, 0, 0))
    mlab.show()


# Plotting the 3D volumetric data using mayavi
plot_3d_volume(x_unique_a, y_unique_a, z_unique_a,
               value_3d_a, "Anisotropic Data")
plot_3d_volume(x_unique_i, y_unique_i, z_unique_i,
               value_3d_i, "Isotropic Data")
