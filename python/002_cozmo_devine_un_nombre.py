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

'''Le Jeu COZMO devine un nombre en Python

Ce script permet à COZMO de tenter de deviner un nombre entre 1 et 100
choisi par le joueur.

COZMO va proposer un nombre, et le joueur devra indiquer à COZMO si le 
nombre à deviner est plus grand (cube bleu), plus petit (cube jaune),
ou celui indiqué par COZMO (cube vert). 
'''

import time
import random

import cozmo
from cozmo.objects import LightCube1Id, LightCube2Id, LightCube3Id
from cozmo.lights import Color, Light
from cozmo.util import degrees, distance_mm, speed_mmps
	
def cozmo_program(robot: cozmo.robot.Robot):

    # Les variables nécessaires 
    min_number = 1
    max_number = 100
    number     = 0
    turn       = 0
    
    # Définir les couleurs 
    light_yellow = Light(Color(name='yellow', rgb = (255, 255, 0)))
    light_green = Light(Color(name='green', rgb = (0, 255, 0)))
    light_blue = Light(Color(name='blue', rgb = (0, 0, 255)))

    # Tourner jusqu'a détecter un visage
    lookaround = robot.start_behavior(cozmo.behavior.BehaviorTypes.FindFaces)
    face = robot.world.wait_for_observed_face()
    lookaround.stop()
    
    # L'hummain trouvé est il connu ou inconnue 
    robot.drive_straight(distance_mm(50), speed_mmps(50)).wait_for_completed()
    if (face.name != ""):
        robot.play_anim_trigger(cozmo.anim.Triggers.AcknowledgeFaceNamed).wait_for_completed()	 
        robot.say_text(face.name).wait_for_completed()
    else:
        robot.play_anim_trigger(cozmo.anim.Triggers.AcknowledgeFaceUnnamed).wait_for_completed()
        robot.say_text("Bonjour").wait_for_completed()
 
    # Donner les explications du jeu 
    robot.say_text("Je vais deviner un nombre entre {} et {}." format(min_number, max_number)).wait_for_completed()
    robot.say_text("Bleu si plus grand.").wait_for_completed()
    robot.world.get_light_cube(LightCube1Id).set_lights(light_blue)
    robot.say_text("Jaune si plus petit.").wait_for_completed()
    robot.world.get_light_cube(LightCube2Id).set_lights(light_yellow)
    robot.say_text("Vert si j'ai trouvé.").wait_for_completed()
    robot.world.get_light_cube(LightCube3Id).set_lights(light_green)
 
    # Jouer l'animation Cozmo content
    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabHappy).wait_for_completed()
    robot.say_text("Vert quand tu es prêt.").wait_for_completed()
    
    # Attendre jusqu'a ce qu'un cube soit touché
    ready = False
    while ready is False:
		target = robot.world.wait_for(cozmo.objects.EvtObjectTapped)
        cube = robot.world.get_light_cube(target.obj.cube_id)
        ready = cube.cube_id is LightCube3Id
 	
    # Générer un nombre aléatoire entre min_number et max_number
    number = random.randint(min_number, max_number)
    found = False;
    cheated = False
    
    # Boucle de jeu
    while found is False and cheated is False:
        turn++
        robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabThinking).wait_for_completed()
        robot.say_text(str(number)).wait_for_completed()
        target = robot.world.wait_for(cozmo.objects.EvtObjectTapped)
        cube = robot.world.get_light_cube(target.obj.cube_id)
        # jouer l'animation suivat le cube touché
        if cube.cube_id is LightCube3Id:
            robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabHappy).wait_for_completed()
            found = True
        elif cube.cube_id is LightCube1Id:
            robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabUnhappy).wait_for_completed()
            min_number = number + 1
        elif cube.cube_id is LightCube2Id:
            robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabUnhappy).wait_for_completed()
            max_number = number - 1
        else:
            cheated = True
        # Le joueur a t'il triché
        if max_number < min_number:
            cheated = True	
        # Tenter de générer un nouveau nombre 
        elif found is False:	
            number = math.round((min_number + max_number) / 2)		

    # Si COZMO à trouvé
    if found is True:
        robot.say_text("{} essais." format(turn)).wait_for_completed()
        robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabWin).wait_for_completed()
    else:
        robot.say_text("Tu as triché").wait_for_completed()
        robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabFrustrated).wait_for_completed()

cozmo.run_program(cozmo_program, use_viewer=True)
