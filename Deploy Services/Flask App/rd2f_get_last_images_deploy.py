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


"""Process to get images online"""

import requests
from bs4 import BeautifulSoup
from datetime import date, datetime
#to sync timezone on los_angeles or place timezone
from pytz import timezone
from rd2f_settings_deploy import TIMEZONE, ARCHIVE_ROOT


import os
import urllib.request

def get_list_cam(save_in_folder=False):
    root_archive = ARCHIVE_ROOT
    
    ### Get to camera folder
    r_folder = requests.get(root_archive)
    #Create a parser of archive webpage
    soup1 = BeautifulSoup(r_folder.text, 'html.parser')
    list_cam = []

    #Go to each camera name -c 
    for link in soup1.find_all('a'):    
        if ("-c" in link.get('href')):
            list_cam.append(link.get('href').replace("/",""))
    date_cam = "list_cam_{}.txt".format(str(date.today()))
    
    if save_in_folder:
        f = open(date_cam, "w")
        for i, cam in enumerate(list_cam): 
            f.write(str(i) + " " + cam + "\n")
        
    return list_cam 



def get_last_image(root_archive, RD2F_root, incrementation, choice): 
    
    root_archive = root_archive
    #timzeone of server
    time_zone = timezone(TIMEZONE)
    
    ### Get to camera folder
    #r_folder = requests.get(url_folder)
    r_folder = requests.get(root_archive)
    soup1 = BeautifulSoup(r_folder.text, 'html.parser')
    
    sources_folder = []
    
    for link in soup1.find_all('a'):    
        if ("-c" in link.get('href')):
            sources_folder.append(root_archive + '/'+ link.get('href') + 'large/')
            
    ### Get to last folder created : that means today
    
    r_folder_cam = requests.get(sources_folder[0])
    soup2 = BeautifulSoup(r_folder_cam.text, 'html.parser')
    
    sources_folder_last = []
    
    #get date of server
    date_timezone = str(datetime.now(time_zone))[0:10]
    
    #!! For now the number into sources_folder is arbitrary
    for link in soup2.find_all('a'):
        if (str(date_timezone).replace('-','') in link.get('href')):
            sources_folder_last.append(sources_folder[choice] + link.get('href'))
    
    #Get the last Q to investigate : we take every links, and we take the last one : it will be the last Q folder. 
    
    r_folder_cam_last = requests.get(sources_folder_last[0])
    soup3 = BeautifulSoup(r_folder_cam_last.text, 'html.parser')
    sources_folder_Q_last = (sources_folder_last[0] + soup3.find_all('a')[-1].get('href'))
    
    
    
        
    ### Get to last image of Q folder
    
    r_folder_Q = requests. get(sources_folder_Q_last)
    soup4 = BeautifulSoup(r_folder_Q.text, 'html.parser')
    
    #<tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="1596276009.jpg">1596276009.jpg</a></td><td align="right">2020-08-01 03:00  </td><td align="right">639K</td><td>&nbsp;</td></tr>
    
    sources = []
    
    for link in soup4.find_all('a'):
        # if ("Parent Directory" in link):
        #     roo = link.get('href')
        
        if (".jpg" in link.get('href')):
            sources.append(sources_folder_Q_last + link.get('href'))
            #print(link.get('href'))
    
    source_last_image = sources[-1]
    
  
    ### Download image
    
    os.chdir(RD2F_root + '\static\last_image_to_test')
    list_cam = get_list_cam()
    urllib.request.urlretrieve(source_last_image, "{}_{}_{:05d}.jpg".format(list_cam[choice],date.today(),incrementation))
    #Creating cache for deploy
    os.chdir(RD2F_root + '\static\cache')
    urllib.request.urlretrieve(source_last_image, "cache.jpg")    
    path_last_img = os.path.join(RD2F_root + '\static\last_image_to_test' + "\{}_{}_{:05d}.jpg".format(list_cam[choice],date.today(),incrementation))
    name = ("{}_{}_{:05d}.jpg".format(list_cam[choice],date.today(),incrementation))
    return path_last_img, name
    
