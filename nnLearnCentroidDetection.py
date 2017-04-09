#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 6 17:49:54 2017

Contains functions that detect centroids of annotations

@author: pgoltstein
"""


########################################################################
### Imports
########################################################################

import numpy as np
import tensorflow as tf
import ImageAnnotation as ia
import iaConvNetTools as cn


########################################################################
# Load data
annotation_size = (27,27)
training_data_path = '/Users/pgoltstein/Dropbox/TEMP/DataSet1'
network_path = '/Users/pgoltstein/Dropbox/TEMP'
print("\nLoading data from directory into training_image_set:")
print(training_data_path)
training_image_set = ia.AnnotatedImageSet()
training_image_set.load_data_dir_tiff_mat(training_data_path)
print(" >> " + training_image_set.__str__())

# Dilate centroids
print("Changing centroid dilation factor of image set to 2")
training_image_set.centroid_dilation_factor = 2

########################################################################
# Set up network
nn = cn.ConvNetCnv2Fc1( \
        input_image_size=annotation_size,
        n_input_channels=training_image_set.n_channels, output_size=(1,2),
        conv1_size=5, conv1_n_chan=16, conv1_n_pool=3,
        conv2_size=5, conv2_n_chan=32, conv2_n_pool=3,
        fc1_n_chan=256, fc1_dropout=0.5, alpha=4e-4 )
nn.start()
nn.load_network_parameters('centroid_net',network_path)

########################################################################
# Train network and save network parameters
nn.train_epochs( training_image_set,
    annotation_type='Centroids', m_samples=500, n_epochs=100)
nn.save_network_parameters('centroid_net',network_path)

########################################################################
# Display performance
print("\nTraining set performance:")
nn.report_F1( training_image_set,
    annotation_type='Centroids', m_samples=2000, show_figure='On')

print('Done!\n')
