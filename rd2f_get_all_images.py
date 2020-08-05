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
from datetime import date

root = 'http://c1.hpwren.uscd.edu/'
root_archive = 'http://c1.hpwren.ucsd.edu/archive/'

### Get to camera folder
#r_folder = requests.get(url_folder)
r_folder = requests.get(root_archive)
soup1 = BeautifulSoup(r_folder.text, 'html.parser')

sources_folder = []

for link in soup1.find_all('a'):    
    if ("-c" in link.get('href')):
        sources_folder.append(root_archive + link.get('href') + 'large/')
        #print(link.get('href'))

### Get to last folder created

r_folder_cam = requests.get(sources_folder[0])
soup2 = BeautifulSoup(r_folder_cam.text, 'html.parser')

sources_folder_last = []
    
for link in soup2.find_all('a'):
    if (str(date.today()).replace('-','') in link.get('href')):
        sources_folder_last.append(sources_folder[35] + link.get('href'))

#Get the last Q to investigate

r_folder_cam_last = requests.get(sources_folder_last[0])
soup3 = BeautifulSoup(r_folder_cam_last.text, 'html.parser')
sources_folder_Q_last = (sources_folder_last[0] + soup3.find_all('a')[-1].get('href'))



    
### Get to last image of Q folder

r_folder_Q = requests. get(sources_folder_Q_last)
soup4 = BeautifulSoup(r_folder_Q.text, 'html.parser')

#<tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="1596276009.jpg">1596276009.jpg</a></td><td align="right">2020-08-01 03:00  </td><td align="right">639K</td><td>&nbsp;</td></tr>

sources = []

for link in soup4.find_all('a'):
    if ("Parent Directory" in link):
        roo = link.get('href')
    
    if (".jpg" in link.get('href')):
        sources.append(root + roo + link.get('href'))
        #print(link.get('href'))
    

