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


import numpy as np
import matplotlib.pyplot as plt

import tensorflow as tf

def predict_image_class(model_to_use, path):
    # Test d'image si necessaire. 
    #image = tf.keras.preprocessing.image.load_img(os.path.join(RD2F_root,'last_image_to_test/00000.jpg'))
    img = tf.keras.preprocessing.image.load_img(path)
    #Affichage de l'image
    plt.imshow(img)
    #Convert img to array
    input_arr = tf.keras.preprocessing.image.img_to_array(img)
    #On resize l'image à la taille demandé par le modèle
    input_arr = tf.image.resize(input_arr, [224,224])
    # Convert single image to a batch.
    input_arr = np.array([input_arr])/255
    
    #Make predictions
    predictions = np.around(model_to_use.predict(input_arr))
    print(model_to_use.predict(input_arr))
    
    if predictions == [[0]]:
        print("No smoke . Class : ", predictions[0])
    else:
        print("Smoke in image / Class : ", predictions[0])