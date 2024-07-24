import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# List of file paths
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

# Extract unique coordinates and reshape the data


def reshape_data(data):
    x_unique = np.unique(data['x'])
    y_unique = np.unique(data['y'])
    z_unique = np.unique(data['z'])

    x_count = len(x_unique)
    y_count = len(y_unique)
    z_count = len(z_unique)
    value_count = data['value'].size
    new_z_count = value_count // (x_count * y_count)

    value_3d = data['value'].values.reshape((x_count, y_count, new_z_count))
    return x_unique, y_unique, z_unique, value_3d


x_unique_a, y_unique_a, z_unique_a, value_3d_a = reshape_data(anisotropic_data)
x_unique_i, y_unique_i, z_unique_i, value_3d_i = reshape_data(isotropic_data)

# Function to plot 3D slices and half-cube views


def plot_3d_slices(x, y, z, data, title, slices, half=False, cmap='viridis'):
    fig = plt.figure(figsize=(15, 10))
    for i, z_slice in enumerate(slices):
        ax = fig.add_subplot(1, len(slices), i + 1, projection='3d')
        X, Y = np.meshgrid(x, y)
        Z = data[:, :, z_slice] if not half else data[:, :len(y)//2, z_slice]
        surf = ax.plot_surface(
            X, Y[:, :len(y)//2] if half else Y, Z, cmap=cmap)
        ax.set_title(f'{title} (Slice {z_slice})')
        fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
    plt.show()


# Define slices to visualize
slices_to_visualize = [0, 25, 50, 75, 99]

# Plotting the selected 3D surface slices
plot_3d_slices(x_unique_a, y_unique_a, z_unique_a, value_3d_a,
               " Anisotropic Data", slices_to_visualize)
plot_3d_slices(x_unique_i, y_unique_i, z_unique_i, value_3d_i,
               " Isotropic Data", slices_to_visualize)

# Plotting half-cube views
plot_3d_slices(x_unique_a, y_unique_a, z_unique_a, value_3d_a,
               "3D Half-Cube Anisotropic Data", slices_to_visualize, half=True)
plot_3d_slices(x_unique_i, y_unique_i, z_unique_i, value_3d_i,
               "Half-Cube Isotropic Data", slices_to_visualize, half=True)
