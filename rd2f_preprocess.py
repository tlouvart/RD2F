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

import os

import tensorflow as tf


from rd2f_settings import *

train_smoke_res_dir = train_smoke_dir
validation_smoke_res_dir = validation_smoke_dir
train_nosmoke_res_dir = train_nosmoke_dir
validation_nosmoke_res_dir = validation_nosmoke_dir

train_smoke_dir = train_smoke_dir.replace('/resized',"")
validation_smoke_dir = validation_smoke_dir.replace('/resized',"")
train_nosmoke_dir = train_nosmoke_dir.replace('/resized',"")
validation_nosmoke_dir = validation_nosmoke_dir.replace('/resized',"")

######## Function listing images in folder

def list_files(path_to_list):
    return [name for name in os.listdir(path_to_list) if name not in {'resized'}]


######## Function rename files

def rename_files(files_to_rename, path_files):
    #get class name
    class_name = os.path.basename(os.path.normpath(path_files))
    #get size
    l = len(files_to_rename)
    
    for i, name in enumerate(files_to_rename):   
        os.rename(os.path.join(path_files,name), os.path.join(path_files,"{}_{:04d}.jpg".format(class_name,i+l+1)))
    
    for j, name in enumerate(list_files(path_files)):
        os.rename(os.path.join(path_files,name), os.path.join(path_files,"{}_{:04d}.jpg".format(class_name,j))) 


######## Function to resize image data : return a list of input array of all files in folder

def resize_files(files_to_rename, path_files, IMG_SIZE):
    list_input_arr = []
    for name in files_to_rename:
        print(name)
        image = tf.keras.preprocessing.image.load_img(os.path.join(path_files,name))
        input_arr = tf.keras.preprocessing.image.img_to_array(image)
        input_arr = tf.image.resize(input_arr, IMG_SIZE) #On resize l'image à la taille demandé par le modèle
        list_input_arr.append(input_arr)
    return list_input_arr

######## Function to save array data into image in target_folder

def save_image(target_folder, list_input_arr):
        #get class name 
        class_name = os.path.basename(os.path.normpath(target_folder))
        for i in range(len(list_input_arr)):
            tf.keras.preprocessing.image.save_img(os.path.join(target_folder,'{}_{:04d}.jpg'.format(class_name,i)), list_input_arr[i], data_format=None, file_format=None, scale=True)
    
######## Function to chage extension of files in a specific folder : input the initial and final extension

def change_ext(folder_to_change, init_ext, final_ext):
    files_to_change = list_files(folder_to_change)
    for name in files_to_change:
        new_name = name.replace(".{}".format(init_ext),".{}".format(final_ext))
        os.rename(os.path.join(folder_to_change, name), os.path.join(folder_to_change, new_name))
                  
 
##### TESTS

# files_train_smoke = list_files(train_smoke_dir)
# files_val_smoke = list_files(validation_smoke_dir)
# files_train_no_smoke = list_files(train_nosmoke_dir)
# files_val_no_smoke = list_files(validation_nosmoke_dir)


# rename_files(files_train_smoke, train_smoke_dir)
# rename_files(files_train_no_smoke, train_nosmoke_dir)
# rename_files(files_val_no_smoke, validation_nosmoke_dir)
# rename_files(files_val_smoke, validation_smoke_dir)


# save_image(train_smoke_res_dir,  resize_files(files_train_smoke, train_smoke_dir, IMG_SIZE))
# save_image(train_nosmoke_res_dir,  resize_files(files_train_no_smoke, train_nosmoke_dir, IMG_SIZE))
# save_image(validation_nosmoke_res_dir,  resize_files(files_val_no_smoke, validation_nosmoke_dir, IMG_SIZE))
# save_image(validation_smoke_res_dir,  resize_files(files_val_smoke, validation_smoke_dir, IMG_SIZE))

    

# files_train_smoke = list_files(train_smoke_dir)
# files_val_smoke = list_files(validation_smoke_dir)
# files_train_no_smoke = list_files(train_nosmoke_dir)
# files_val_no_smoke = list_files(validation_nosmoke_dir)