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


"""Ce fichier a pour objectif d'effectuer un preprocessing des images télechargées"""

import sys
import os

import numpy as np


import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator




train_smoke_dir = 'Datasets/Images/train/smoke'  
train_nosmoke_dir = 'Datasets/Images/train/no_smoke'  
validation_smoke_dir = 'Datasets/Images/validate/smoke' 
validation_nosmoke_dir = 'Datasets/Images/validate/no_smoke'

#sys.path.insert(0, os.path.join(RD2F_root, 'lib'))
#sys.path.insert(0, RD2F_root)

files_train_smoke = [name for name in os.listdir(train_smoke_dir) if name not in {'resized'}]
files_val_smoke = [name for name in os.listdir(validation_smoke_dir) if name not in {'resized'}]

files_train_no_smoke = [name for name in os.listdir(train_nosmoke_dir) if name not in {'resized'}]
files_val_no_smoke = [name for name in os.listdir(validation_nosmoke_dir) if name not in {'resized'}]

######### On change les extensions

#for name in files_smoke:
#    new_name = name.replace(".jpeg",".jpg")
#    os.rename(os.path.join(datasets_smoke,name),os.path.join(datasets_smoke,new_name))

#On change le nom des données dans les deux datasets
j=0
for i, name in enumerate(files_train_smoke):
    
    
    image = tf.keras.preprocessing.image.load_img(os.path.join(train_smoke_dir,name))
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = tf.image.resize(input_arr, [224,224]) #On resize l'image à la taille demandé par le modèle
    tf.keras.preprocessing.image.save_img(os.path.join(train_smoke_dir,'resized/res_smoke_{:04d}.jpg'.format(i)), input_arr, data_format=None, file_format=None, scale=True)
    
    if (name != "smoke_{:04d}.jpg".format(i)):
        os.rename(os.path.join(train_smoke_dir,name), os.path.join(train_smoke_dir,"smoke_{:04d}.jpg".format(i)))
        os.rename(os.path.join(train_smoke_dir,os.path.join(train_smoke_dir,"smoke_{:04d}.jpg".format(i))), os.path.join(train_smoke_dir,"smoke_{:04d}.jpg".format(j)))
        j += 1
    else:
        j += 1
        pass

j=0
for i, name in enumerate(files_train_no_smoke):
    
    
    image = tf.keras.preprocessing.image.load_img(os.path.join(train_nosmoke_dir,name))
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = tf.image.resize(input_arr, [224,224]) #On resize l'image à la taille demandé par le modèle
    tf.keras.preprocessing.image.save_img(os.path.join(train_nosmoke_dir,'resized/res_no_smoke_{:04d}.jpg'.format(i)), input_arr, data_format=None, file_format=None, scale=True)
    
    if (name != "smoke_{:04d}.jpg".format(i)):
        os.rename(os.path.join(train_nosmoke_dir,name), os.path.join(train_nosmoke_dir,"smoke_{:04d}.jpg".format(i)))
        os.rename(os.path.join(train_nosmoke_dir,os.path.join(train_nosmoke_dir,"smoke_{:04d}.jpg".format(i))), os.path.join(train_nosmoke_dir,"smoke_{:04d}.jpg".format(j)))
        j += 1
    else:
        j += 1
        pass
    
for i, name in enumerate(files_val_smoke):
        
    image = tf.keras.preprocessing.image.load_img(os.path.join(validation_smoke_dir,name))
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = tf.image.resize(input_arr, [224,224]) #On resize l'image à la taille demandé par le modèle
    tf.keras.preprocessing.image.save_img(os.path.join(validation_smoke_dir,'resized/res_smoke_{:04d}.jpg'.format(i)), input_arr, data_format=None, file_format=None, scale=True)
    
for i, name in enumerate(files_val_no_smoke):
        
    image = tf.keras.preprocessing.image.load_img(os.path.join(validation_nosmoke_dir,name))
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = tf.image.resize(input_arr, [224,224]) #On resize l'image à la taille demandé par le modèle
    tf.keras.preprocessing.image.save_img(os.path.join(validation_nosmoke_dir,'resized/res_smoke_{:04d}.jpg'.format(i)), input_arr, data_format=None, file_format=None, scale=True)
       
    
    

files_train_smoke = [name for name in os.listdir(train_smoke_dir)]
files_val_smoke = [name for name in os.listdir(validation_smoke_dir)]

files_train_no_smoke = [name for name in os.listdir(train_nosmoke_dir)]
files_val_no_smoke = [name for name in os.listdir(validation_nosmoke_dir)]
