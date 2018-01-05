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

import cozmo
from cozmo.objects import LightCube1Id, LightCube2Id, LightCube3Id
from cozmo.lights import Color, Light
from cozmo.util import degrees, distance_mm, speed_mmps

# index de la couleur utilisée pour chaque cube
idx1 = 0
idx2 = 0
idx3 = 0	

def cube1Tapped():
    idx1 += 1
    raise events.StopProgation

def cube2Tapped():
    idx2 += 1
    raise events.StopProgation

def cube3Tapped():
    idx3 += 1
    raise events.StopProgation
    
def cozmo_program(robot: cozmo.robot.Robot):

    colors = [
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
    cube1.add_event_handler(cozmo.objects.EvtObjectTapped, cube1Tapped)
         
    cube2 = robot.world.get_light_cube(LightCube2Id)
    cube2.add_event_handler(cozmo.objects.EvtObjectTapped, cube2Tapped)

    cube3 = robot.world.get_light_cube(LightCube3Id)
    cube3.add_event_handler(cozmo.objects.EvtObjectTapped, cube3Tapped)
    
    lookaround = robot.start_behavior(cozmo.behavior.BehaviorTypes.FindFaces)

    while idx1 < 8 and  idx2 < 8 and idx3 < 8:
        cube1.set_lights(color[idx1])
        cube2.set_lights(color[idx2])
        cube3.set_lights(color[idx3])

    lookaround.stop()
    
cozmo.run_program(cozmo_program, use_viewer=True)
    
