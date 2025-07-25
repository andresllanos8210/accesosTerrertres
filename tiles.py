# -*- coding: utf-8 -*-
"""tiles.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1y9dg58QVuN2NN53kLpWmKO9yaRDvxUHU
"""

from google.colab import drive
drive.mount('/content/drive', force_remount=True)
from google.colab import files

! pip install GeoTile

! pip install fiona

from tqdm import tqdm
from geotile import GeoTile
import os
import numpy as np

imgTrain = ('/content/drive/MyDrive/GEE_Exports/18NWH-2025.tif')
viasTrain = ('/content/drive/MyDrive/GEE_Exports/Acceso2017-18NWH.shp')
imgTest = ('/content/drive/MyDrive/GEE_Exports/18NXH-2025.tif')
# viasTrain = ('/content/drive/MyDrive/GEE_Exports/ViasTrain1.shp')

train = GeoTile(imgTrain)
train.meta

# Create the output directory if it doesn't exist
output_dir = '/content/drive/MyDrive/GEE_Exports/trainTiles'
os.makedirs(output_dir, exist_ok=True)

train.generate_tiles('/content/drive/MyDrive/GEE_Exports/trainTiles', prefix='train_', tile_x=256, tile_y=256, stride_x=256, stride_y=256)

# Create the output directory if it doesn't exist
output_dir = '/content/drive/MyDrive/GEE_Exports/viasTrain'
os.makedirs(output_dir, exist_ok=True)

train.rasterization(viasTrain, '/content/drive/MyDrive/GEE_Exports/viasTrain/viasTrain.tif')

train_y = GeoTile('/content/drive/MyDrive/GEE_Exports/viasTrain/viasTrain.tif')
train_y.generate_tiles('/content/drive/MyDrive/GEE_Exports/viasTrain', prefix='test_', tile_x=256, tile_y=256, stride_x=256, stride_y=256)

test = GeoTile(imgTest)
test.meta

# Create the output directory if it doesn't exist
output_dir = '/content/drive/MyDrive/GEE_Exports/testTiles'
os.makedirs(output_dir, exist_ok=True)

test.generate_tiles('/content/drive/MyDrive/GEE_Exports/testTiles', prefix='test_', tile_x=256, tile_y=256, stride_x=256, stride_y=256)

# generate tiles and store it in drive se genera el cubo de datos con los tiles de S2 de train
# Setting save_tiles=False to load tile data into memory as a numpy array
train.generate_tiles(save_tiles=False, tile_x=256, tile_y=256, stride_x=256, stride_y=256)

# generate tiles and store it in drive se genera el cubo de datos con los tiles de las mascaras de vias
train_y.generate_tiles(save_tiles=False, tile_x=256, tile_y=256, stride_x=256, stride_y=256)

# generate tiles and store it in drive se genera el cubo de datos con los tiles de las mascaras de test
test.generate_tiles(save_tiles=False, tile_x=256, tile_y=256, stride_x=256, stride_y=256)

train.tile_data.min(), train.tile_data.max(), #test.tile_data.mean()

test.tile_data.min(), test.tile_data.max(), #test.tile_data.mean()

train.convert_nan_to_zero()

# preprocessing (eg. convert nan to zero and normalization of tiles)
test.convert_nan_to_zero()
# gt_train.normalize_tiles()

train.normalize_tiles()

test.normalize_tiles()

train.tile_data.min(), train.tile_data.max()

test.tile_data.min(), test.tile_data.max()

test.tile_data.shape

test.tile_data.min(), test.tile_data.max()

train.save_numpy('/content/drive/MyDrive/GEE_Exports/trainTiles.npy')

test.save_numpy('/content/drive/MyDrive/GEE_Exports/testTiles.npy')

train_y.save_numpy('/content/drive/MyDrive/GEE_Exports/viasTrain.npy')

# # generate tiles and store it inside geotile package
# gt_test.generate_tiles(save_tiles=False)
# gt_test_y.generate_tiles(save_tiles=False)

# # preprocessing (eg. convert nan to zero and normalization of tiles)
# gt_test.convert_nan_to_zero()
# gt_test.normalize_tiles()

# # save it as a numpy array
# gt_test.save_numpy('/content/drive/MyDrive/Colab Notebooks/Resultados/X_test.npy')
# gt_test_y.save_numpy('/content/drive/MyDrive/Colab Notebooks/Resultados/y_test.npy')

X_train = np.load('/content/drive/MyDrive/GEE_Exports/trainTiles.npy')
X_train.max(), X_train.min(), X_train.dtype, X_train.shape

y_train= np.load('/content/drive/MyDrive/GEE_Exports/viasTrain.npy')

import matplotlib.pyplot as plt

# Let's plot a few sample input RGB images and output images with masks
num_samples = 2  # Number of samples to display
fig, axes = plt.subplots(num_samples, 2, figsize=(10, num_samples * 5)) # Create a grid of subplots

for i in range(num_samples):
    img_index = np.random.randint(0, X_train.shape[0]) # Get a random index

    # Display the image
    axes[i, 0].imshow(X_train[img_index]) # Corrected indexing

    axes[i, 0].set_title(f"Image {img_index}")
    axes[i, 0].axis('on') # Hide axes ticks

    # Display the mask
    # Use a colormap that makes the mask clearly visible, e.g., 'gray' or 'binary'
    axes[i, 1].imshow(y_train[img_index, :, :, 0], cmap='gray') # Corrected indexing for mask
    axes[i, 1].set_title(f'Mask {img_index}')
    axes[i, 1].axis('on') # Hide axes ticks

plt.tight_layout() # Adjust layout to prevent titles overlapping
plt.show()

# Select a random sample index
sample_index = np.random.randint(0, y_train.shape[0])

# Get the mask for the selected sample
# Assuming y_train has a shape like (num_samples, height, width, num_channels)
# and the mask is in the first channel
mask_to_display = y_train[sample_index, :, :, 0]

# Display the mask
plt.figure(figsize=(6, 6))
plt.imshow(mask_to_display, cmap='gray') # Use 'gray' colormap for masks
plt.title(f'Mask Sample {sample_index}')
# plt.axis('on') # Hide axes ticks
plt.show()

# import matplotlib.pyplot as plt

# Let's plot a sample input RGB image and output image with buildings
fig, (ax1, ax2) = plt.subplots(1,2)
img = np.random.randint(0, X_train.shape[0]) # Use the actual number of samples
print(img)
ax1.imshow(X_train[img]) # Select first 3 bands and transpose for imshow
ax2.imshow(y_train[img, :, :, 0], cmap='gray')
ax1.set_title(f"Image  {img}")
ax2.set_title(f'Mask {img}')
plt.show()

# import tensorflow as tf
# print(tf.config.list_physical_devices('GPU'))

