# Copyright 2020 RD2F PROJECT, Theophile LOUVART
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================


""" Processing datasets and training model to detect either there is smoke or not in images """

import os

import numpy as np
import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow.keras.models import Sequential

from tensorflow.keras import models
from tensorflow.keras import layers

from tensorflow.keras.layers import Dense, Conv2D, Flatten, MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam

#Import dependancies of RD2F Project

from rd2f_settings import *


#Image augment: It allows an expansion of our dataset, rescaling data for better processing
# and lower the calculation time
train_image_generator = ImageDataGenerator(rescale=1./255) #Generator for train data

val_image_generator = ImageDataGenerator(rescale=1./255) # Generator for validation data

#Batchs of augmented datas

train_data_generator = train_image_generator.flow_from_directory(train_image_folder,
                                                           batch_size=batch_size,
                                                           target_size=(h_image, w_image),
                                                           class_mode=cmode)


val_data_generator = val_image_generator.flow_from_directory(validate_image_folder,
                                                              batch_size=batch_size,
                                                              target_size=(h_image, w_image),
                                                              class_mode=cmode)


#### Custom Model for RD2F purposes

model = Sequential([
    Conv2D(16, (3,3), activation='relu', input_shape=(h_image, w_image ,3)),
    MaxPooling2D(2,2),
    Conv2D(32, (3,3), activation='relu'),
    MaxPooling2D(2,2),
    Conv2D(64, (3,3), activation='relu'),
    MaxPooling2D(2,2),
    Flatten(),
    #It seems that a dense layer with more neurons gives a worse accuracy 
    Dense(516, activation='relu'),
    Dense(258, activation='relu'),
    Dense(1, activation='sigmoid')
])

#### Optimizers : Adam and Loss : binary_crossentropy

model.compile(optimizer=Adam(lr=0.001),
              loss='binary_crossentropy',
              metrics=['accuracy'])



#### TRAINING
history = model.fit(train_data_generator,steps_per_epoch=size_train // batch_size,epochs=nb_epoch,
    validation_data=val_data_generator,validation_steps=size_val // batch_size,verbose=1)

#Show a progress bar with verbose=1, silent with 0

#### Saving Model

path = os.path.join(RD2F_root, "{rd2f_model.h5}")
model.save(path)

