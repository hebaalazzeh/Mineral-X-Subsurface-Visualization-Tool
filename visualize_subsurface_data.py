"""
Subsurface Visualization Tool
Created by: Heba Alazzeh
Function: This script loads, processes, and visualizes 3D subsurface data from multiple anisotropic and isotropic CSV files. 
          The tool allows users to toggle between different visualization modes: standard view, interactive slicing, and structure identification.
Last Updated: 08/10/2024
"""

import pandas as pd
import numpy as np
from mayavi import mlab
from traits.api import HasTraits, Instance, Enum, Button
from traitsui.api import View, Item, Group, HGroup, VGroup
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, SceneEditor

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

# The Visualization Tool


class VisualizationTool(HasTraits):
    scene = Instance(MlabSceneModel, ())
    view_mode = Enum("Standard", "Interactive Slicing",
                     "Structure Identification")
    update_view = Button("Update View")

    def __init__(self):
        super(VisualizationTool, self).__init__()
        self.plot_data = None
        self.x = None
        self.y = None
        self.z = None

    def _view_mode_changed(self):
        self.update_visualization()

    def _update_view_fired(self):
        self.update_visualization()

    def update_visualization(self):
        self.scene.mlab.clf()  # Clear the scene

        if self.view_mode == "Standard":
            self.plot_standard()
        elif self.view_mode == "Interactive Slicing":
            self.plot_slicing()
        elif self.view_mode == "Structure Identification":
            self.plot_structures()

    def plot_standard(self):
        self.plot_data = mlab.pipeline.scalar_field(
            self.x, self.y, self.z, self.data)
        mlab.pipeline.volume(self.plot_data)
        mlab.axes(color=(0, 0, 0))
        mlab.title(f"{self.title} - Standard View", size=0.5, color=(0, 0, 0))

    def plot_slicing(self):
        self.plot_data = mlab.pipeline.scalar_field(
            self.x, self.y, self.z, self.data)
        mlab.pipeline.volume(self.plot_data)
        mlab.pipeline.image_plane_widget(
            self.plot_data, plane_orientation='x_axes', slice_index=self.x.shape[0] // 2)
        mlab.pipeline.image_plane_widget(
            self.plot_data, plane_orientation='y_axes', slice_index=self.y.shape[1] // 2)
        mlab.pipeline.image_plane_widget(
            self.plot_data, plane_orientation='z_axes', slice_index=self.z.shape[2] // 2)
        mlab.axes(color=(0, 0, 0))
        mlab.title(f"{self.title} - Interactive Slicing",
                   size=0.5, color=(0, 0, 0))

    def plot_structures(self):
        self.plot_data = mlab.pipeline.scalar_field(
            self.x, self.y, self.z, self.data)
        threshold = mlab.pipeline.threshold(self.plot_data, low=self.threshold)
        mlab.pipeline.surface(threshold, colormap='viridis')
        mlab.axes(color=(0, 0, 0))
        mlab.title(f"{self.title} - Structure Identification",
                   size=0.5, color=(0, 0, 0))

    def set_data(self, x, y, z, data, title, threshold=4.0):
        self.x, self.y, self.z = np.meshgrid(x, y, z, indexing='ij')
        self.data = data
        self.title = title
        self.threshold = threshold
        self.update_visualization()

    view = View(
        VGroup(
            HGroup(
                Item('view_mode', label="Visualization Mode"),
                Item('update_view', show_label=False),
            ),
            Group(
                Item('scene',
                     editor=SceneEditor(scene_class=MayaviScene),
                     height=500, width=700, show_label=False),
            ),
        ),
        resizable=True,
        title="Subsurface Visualization Tool",
    )


# Instantiate the visualization tool
viz_tool = VisualizationTool()

# Set anisotropic data as default, and allow toggle between modes
viz_tool.set_data(x_unique_a, y_unique_a, z_unique_a,
                  value_3d_a, "Anisotropic Data")

# To show isotropic data, call:
# viz_tool.set_data(x_unique_i, y_unique_i, z_unique_i, value_3d_i, "Isotropic Data")

viz_tool.configure_traits()
