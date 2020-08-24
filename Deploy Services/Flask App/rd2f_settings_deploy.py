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
TIMEZONE = 'America/Los_Angeles'
ARCHIVE_ROOT = 'http://c1.hpwren.ucsd.edu/archive'
MON_UPDATE_RATE = 30000
DASH_UPDATE_RATE = 30000