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


#Import fro Confusion matrix
from sklearn.metrics import classification_report, confusion_matrix
import itertools


#Import dependancies of RD2F Project

from rd2f_settings import *



def train_model(train_image_folder,validate_image_folder,batch_size,IMG_SIZE,cmode,size_train,size_val,nb_epoch):

    #Image augment: It allows an expansion of our dataset, rescaling data for better processing
    # and lower the calculation time
    train_image_generator = ImageDataGenerator(rescale=1./255) #Generator for train data
    
    val_image_generator = ImageDataGenerator(rescale=1./255) # Generator for validation data
    
    #Batchs of augmented datas
    
    train_data_generator = train_image_generator.flow_from_directory(train_image_folder,
                                                               batch_size=batch_size,
                                                               target_size=IMG_SIZE,
                                                               class_mode=cmode)
    
    
    val_data_generator = val_image_generator.flow_from_directory(validate_image_folder,
                                                                  batch_size=batch_size,
                                                                  target_size=IMG_SIZE,
                                                                  class_mode=cmode,
                                                                  shuffle=False)
    
    
    #### Custom Model for RD2F purposes
    
    model = Sequential([
        Conv2D(16, (3,3), activation='relu', input_shape=(IMG_SIZE[0],IMG_SIZE[1],3)),
        MaxPooling2D(2,2),
        Conv2D(32, (3,3), activation='relu'),
        MaxPooling2D(2,2),
        Conv2D(64, (3,3), activation='relu'),
        MaxPooling2D(2,2),
        Flatten(),
        #It seems that a dense layer with more neurons gives a worse accuracy 
        Dense(512, activation='relu'),
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
    
    
    #Confution Matrix and Classification Report
    Y_pred = model.predict_generator(val_data_generator, size_val)
    y_pred = np.around(Y_pred)
    # print('Confusion Matrix')
    # print(Y_pred)
    # print(y_pred2)
    # print(val_data_generator.classes.shape)
    cm = confusion_matrix(val_data_generator.classes, y_pred)

    return model, history, cm


#### Saving Model

def save_model(model, path_to_save):
    #path = os.path.join(RD2F_root, "{rd2f_model.h5}")
    model.save(path_to_save)

def plot_confusion_matrix(cm, classes,
                        normalize=False,
                        title='Confusion matrix',
                        cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
            horizontalalignment="center",
            color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

out_model,history,conf= train_model(train_image_folder,validate_image_folder,batch_size,IMG_SIZE,cmode,size_train,size_val,nb_epoch)
save_model(out_model, os.path.join(RD2F_root, "{rd2f_model.h5}"))
plot_confusion_matrix(conf, ['No Smoke','Smoke'])
