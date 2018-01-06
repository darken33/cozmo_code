#!/usr/bin/env python3

# Copyright (c) 2018 Philippe Bousquet <darken33@free.fr>.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License in the file LICENSE.txt or at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''Test des Event Handler de COZMO'''

import time

import cozmo
from cozmo.objects import LightCube1Id, LightCube2Id, LightCube3Id
from cozmo.lights import Color, Light
from cozmo.util import degrees, distance_mm, speed_mmps

# index de la couleur utilisée pour chaque cube
idx1 = 0
idx2 = 0
idx3 = 0	
robot = None
color = []

def cubeTapped(evt, *, obj, tap_count, tap_duration, tap_intensity, **kwargs):
    global idx1
    global idx2
    global idx3    
    global robot    
    global color
    if (obj.cube_id is LightCube1Id):
        idx1 += 1
        robot.world.get_light_cube(LightCube1Id).set_lights(color[idx1])
    elif (obj.cube_id is LightCube2Id):    
        idx2 += 1
        robot.world.get_light_cube(LightCube2Id).set_lights(color[idx2])
    elif (obj.cube_id is LightCube3Id):    
        idx3 += 1
        robot.world.get_light_cube(LightCube3Id).set_lights(color[idx3])
   
def cozmo_program(_robot: cozmo.robot.Robot):

    global idx1
    global idx2
    global idx3    
    global robot
    global color
    
    idx1 = 0
    idx2 = 0
    idx3 = 0
    robot = _robot
    
    color = [
        Light(Color(rgb = (0, 0, 0))),
        Light(Color(rgb = (0, 0, 255))),
        Light(Color(rgb = (0, 255, 0))),
        Light(Color(rgb = (0, 255, 255))),
        Light(Color(rgb = (255, 0, 0))),
        Light(Color(rgb = (255, 0, 255))),
        Light(Color(rgb = (255, 255, 0))),
        Light(Color(rgb = (255, 255, 255)))
    ]
    
    cube1 = robot.world.get_light_cube(LightCube1Id)      
    cube2 = robot.world.get_light_cube(LightCube2Id)
    cube3 = robot.world.get_light_cube(LightCube3Id)
    
    robot.world.add_event_handler(cozmo.objects.EvtObjectTapped, cubeTapped)
#    lookaround = robot.start_behavior(cozmo.behavior.BehaviorTypes.FindFaces)

    while idx1 < 8 and  idx2 < 8 and idx3 < 8:
        time.sleep(1)
        
#    lookaround.stop()
    
cozmo.run_program(cozmo_program, use_viewer=True)
    
