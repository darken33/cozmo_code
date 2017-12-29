#!/usr/bin/env python3

# Copyright (c) 2017 Philippe Bousquet <darken33@free.fr>.
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

'''Le Tour Rapporte COZMO en Python

Ce script permet à COZMO de se comporter comme un chien qui joue à la
balle.

COZMO va repérer un vizage humain, puis se dirriger vers lui, il va alors
jouer l'animation correspondant à l'animal, attendre qu'on lui indique 
un cube à aller cercher, puis aller le rammasser et le rapporter. 
'''

import time

import cozmo
from cozmo.objects import LightCube1Id, LightCube2Id, LightCube3Id
from cozmo.lights import Color, Light
from cozmo.util import degrees, distance_mm, speed_mmps
	
def cozmo_program(robot: cozmo.robot.Robot):

    # Définir la couleur jaune
    light_yellow = Light(Color(name='yellow', rgb = (255, 255, 0)))
    light_cyan = Light(Color(name='cyan', rgb = (0, 255, 255)))

    # Tourner jusqu'a détecter un visage
    lookaround = robot.start_behavior(cozmo.behavior.BehaviorTypes.FindFaces)
    face = robot.world.wait_for_observed_face()
    lookaround.stop()

    # Jouer l'animation du Chien
    robot.drive_straight(distance_mm(150), speed_mmps(50)).wait_for_completed()
    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabDog).wait_for_completed()
    
    # Se connecter aux différents cubes et les faire clignoter en jaune
    robot.world.get_light_cube(LightCube1Id).set_lights(light_yellow.flash())
    robot.world.get_light_cube(LightCube2Id).set_lights(light_yellow.flash())
    robot.world.get_light_cube(LightCube3Id).set_lights(light_yellow.flash())

    # Attendre jusqu'a ce qu'un cube soit touché
    target = robot.world.wait_for(cozmo.objects.EvtObjectTapped)
    cube = robot.world.get_light_cube(target.obj.cube_id)
    robot.world.get_light_cube(LightCube1Id).set_lights(light_cyan)
    robot.world.get_light_cube(LightCube2Id).set_lights(light_cyan)
    robot.world.get_light_cube(LightCube3Id).set_lights(light_cyan)
    cube.set_lights(light_yellow)
	
    # Tourner jusqu'a détecter le cube
    found = False;
    lookaround = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
    while found is False:
        tcube = robot.world.wait_for_observed_light_cube(include_existing=False)
        found = tcube is cube
    lookaround.stop()
		
    # Rammasser le cube
    robot.dock_with_cube(cube, approach_angle=cozmo.util.degrees(180), num_retries=3).wait_for_completed()
    robot.move_lift(0.2)
 	
    # Tourner jusqu'a détecter de nouvea le visage précédent
    found = False;
    lookaround = robot.start_behavior(cozmo.behavior.BehaviorTypes.FindFaces)
    while found is False:
        tface = robot.world.wait_for_observed_face()
        found = tface is face
    lookaround.stop()

    # Se déplacer vers le visage poser le cube 
    robot.drive_straight(distance_mm(200), speed_mmps(50)).wait_for_completed()
    robot.move_lift(-3)
    robot.move_lift(0)
    robot.drive_straight(distance_mm(-100), speed_mmps(50)).wait_for_completed()
    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabDog).wait_for_completed()

cozmo.run_program(cozmo_program, use_viewer=True)
