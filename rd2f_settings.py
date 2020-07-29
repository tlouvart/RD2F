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

"Settings of application rd2f"

import os

#Paths
RD2F_root = os.path.dirname(os.path.abspath(__file__))

directory = os.path.join(RD2F_root, 'Datasets\Images_gridded')

#1ere option

# train_image_folder ='Datasets/Images_gridded/train'
# validate_image_folder = 'Datasets/Images_gridded/validate'

# train_smoke_dir = 'Datasets/Images_gridded/train/grid_smoke'  
# train_nosmoke_dir = 'Datasets/Images_gridded/train/grid_no_smoke'  
# validation_smoke_dir = 'Datasets/Images_gridded/validate/grid_smoke' 
# validation_nosmoke_dir = 'Datasets/Images_gridded/validate/grid_no_smoke'

#2eme option

train_image_folder ='Datasets/Images/train'
validate_image_folder = 'Datasets/Images/validate'

train_smoke_dir = 'Datasets/Images/train/smoke/resized'  
train_nosmoke_dir = 'Datasets/Images/train/no_smoke/resized'  
validation_smoke_dir = 'Datasets/Images/validate/smoke/resized' 
validation_nosmoke_dir = 'Datasets/Images/validate/no_smoke/resized'





#Size of datasets
size_train = len(os.listdir(train_smoke_dir)) + len(os.listdir(train_nosmoke_dir))
size_val = len(os.listdir(validation_smoke_dir)) + len(os.listdir(validation_nosmoke_dir))

#Parameters
h_image = 224
w_image = 224
cmode = 'binary'

#Batch and epochs
nb_epoch = 5
batch_size = 30

