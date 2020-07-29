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


""" Ce fichier a pour objectif de charger un modèle et de le tester sur des images de tests
Chargement de modèle rd2f """


import os

import numpy as np
import matplotlib.pyplot as plt

import tensorflow as tf

#Import dependancies of rd2f project
from rd2f_settings import *


#Importation du modèle entrainé 
Loaded_model = tf.keras.models.load_model('{rd2f_model.h5}')


# Test d'image si necessaire. 
image = tf.keras.preprocessing.image.load_img(os.path.join(RD2F_root,'test/test_encore/1528756506_-00900.jpg'))

#Affichage de l'image
plt.imshow(image)


input_arr = tf.keras.preprocessing.image.img_to_array(image)
input_arr = tf.image.resize(input_arr, [224,224]) #On resize l'image à la taille demandé par le modèle
input_arr = np.array([input_arr])  # Convert single image to a batch.


predictions = Loaded_model.predict(input_arr)
if predictions == [[0]]:
    print("No smoke")
else:
    print("Smoke in image")