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

'''Jeu Speed Cube
Ce jeu peut se jouer jusqu'à trois joueurs, chacun tape un cube le plus 
rapidement possible. Le premier à avoir tapé le cube 7 fois a gagné.
'''

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
    if (obj.cube_id is LightCube1Id and idx1 < 7 and idx2 < 7 and idx3 < 7):
        idx1 += 1
        robot.world.get_light_cube(LightCube1Id).set_lights(color[idx1])
    elif (obj.cube_id is LightCube2Id and idx1 < 7 and idx2 < 7 and idx3 < 7):    
        idx2 += 1
        robot.world.get_light_cube(LightCube2Id).set_lights(color[idx2])
    elif (obj.cube_id is LightCube3Id and idx1 < 7 and idx2 < 7 and idx3 < 7):    
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
    
    robot.world.get_light_cube(LightCube1Id).set_lights(color[idx1])      
    robot.world.get_light_cube(LightCube2Id).set_lights(color[idx2])
    robot.world.get_light_cube(LightCube3Id).set_lights(color[idx3])

    robot.play_anim_trigger(cozmo.anim.Triggers.BouncerIdeaToPlay).wait_for_completed()
    robot.say_text("Salut").wait_for_completed()
    robot.say_text("Nous allons jouer à Speed Cube").wait_for_completed()
    robot.say_text("Ce jeu peut se jouer jusqu'à trois joueurs").wait_for_completed()    
    robot.say_text("Le joueur 1 jouera avec le cube 1").wait_for_completed()    
    robot.world.get_light_cube(LightCube1Id).set_lights(color[2].flash())      
    time.sleep(1)
    robot.world.get_light_cube(LightCube1Id).set_lights(color[idx1])      
    robot.say_text("Le joueur 2 jouera avec le cube 2").wait_for_completed()    
    robot.world.get_light_cube(LightCube2Id).set_lights(color[2].flash())      
    time.sleep(1)
    robot.world.get_light_cube(LightCube2Id).set_lights(color[idx2])      
    robot.say_text("Le joueur 3 jouera avec le cube 3").wait_for_completed()    
    robot.world.get_light_cube(LightCube3Id).set_lights(color[2].flash())      
    time.sleep(1)
    robot.world.get_light_cube(LightCube3Id).set_lights(color[idx3])      
    robot.say_text("Le premier qui aura tappé 7 fois le cube aura gagné !").wait_for_completed()    
    time.sleep(1)
    robot.say_text("Attention").wait_for_completed()    
    time.sleep(1)
    robot.say_text("Prêt ?").wait_for_completed()    
    time.sleep(1)
    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLab123Go).wait_for_completed()
     
    robot.world.add_event_handler(cozmo.objects.EvtObjectTapped, cubeTapped)
    while idx1 < 7 and  idx2 < 7 and idx3 < 7:
        time.sleep(0.01)
    
    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabHappy).wait_for_completed()
    if (idx1 == 7):
        robot.say_text("Vainqueur joueur 1 !").wait_for_completed()    
    elif (idx2 == 7):
        robot.say_text("Vainqueur joueur 2 !").wait_for_completed()    
    else:
        robot.say_text("Vainqueur joueur 3 !").wait_for_completed()    
            
    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabWin).wait_for_completed()
    
cozmo.run_program(cozmo_program, use_viewer=True)
    
