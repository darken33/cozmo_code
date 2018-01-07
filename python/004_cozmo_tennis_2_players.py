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

'''COZMO Tennis For 2 Players

Ce programme se veut un jeu de tennis se jouant à deux joueurs.
Il reprend les principes du jeu tennis disponnible à l'époque sur le
Microcomputer Training vendu dans les magasins Tandy au début des années
90.

'''

import time
import asyncio
import cozmo
from cozmo.objects import LightCube1Id, LightCube2Id, LightCube3Id
from cozmo.lights import Color, Light
from cozmo.util import degrees, distance_mm, speed_mmps

# Définir les couleurs
light_yellow = Light(Color(name='yellow', rgb = (255, 255, 0))) # balle
light_gray = Light(Color(name='gray', rgb = (200, 200, 200)))   # filet
light_blue = Light(Color(name='blue', rgb = (0, 0, 255)))       # joueur2
light_red = Light(Color(name='red', rgb = (255, 0, 0)))         # joueur1 
light_off = Light(Color(name='off', rgb = (0, 0, 0))) 

robot = None

ball_position = 0
ball_speed = 0.5
ball_direction = 1

cube1 = None 
cube2 = None
cube3 = None

ready = False

def isReady(evt, *, obj, tap_count, tap_duration, tap_intensity, **kwargs):
    global ready
    ready = True
    
def draw_field_intro():
    # variables globales
    global light_gray
    global light_blue
    global light_red 
    global light_off 
    global robot
    global cube1
    global cube2
    global cube3
     
    # Les cubes représentent le terrain de jeu
    cube1.set_lights(light_off)
    cube2.set_lights(light_off)
    cube3.set_lights(light_off)
    time.sleep(1)	
    cube1.set_light_corners(light_red, light_off, light_off, light_off)
    time.sleep(1)
    cube1.set_light_corners(light_red, light_off, light_red, light_off)
    time.sleep(1)
    cube2.set_light_corners(light_red, light_off, light_off, light_off)
    time.sleep(1)
    cube2.set_light_corners(light_red, light_gray, light_off, light_gray)
    time.sleep(1)
    cube2.set_light_corners(light_red, light_gray, light_blue, light_gray)
    time.sleep(1)
    cube3.set_light_corners(light_blue, light_off, light_off, light_off)
    time.sleep(1)
    cube3.set_light_corners(light_blue, light_off, light_blue, light_off)
    time.sleep(1)

def draw_field():
    # variables globales
    global light_gray
    global light_blue
    global light_red 
    global light_off 
    global robot
    global cube1
    global cube2
    global cube3

    # Afficher le terrain de tennis
    cube1.set_light_corners(light_red, light_off, light_red, light_off)
    cube2.set_light_corners(light_red, light_gray, light_blue, light_gray)
    cube3.set_light_corners(light_blue, light_off, light_blue, light_off)

def draw_ball():
    # variables globales
    global light_yellow
    global light_gray
    global light_blue
    global light_red 
    global light_off 
    global robot
    global cube1
    global cube2
    global cube3

    # Afficher la balle suivant sa position
    if (ball_position == 0):
        cube1.set_light_corners(light_yellow, light_off, light_red, light_off)
    elif (ball_position == 1):   
        cube1.set_light_corners(light_red, light_off, light_yellow, light_off)
    elif (ball_position == 2):   
        cube2.set_light_corners(light_yellow, light_gray, light_blue, light_gray)
    elif (ball_position == 3):   
        cube2.set_light_corners(light_red, light_yellow, light_blue, light_yellow)
    elif (ball_position == 4):   
        cube2.set_light_corners(light_red, light_gray, light_yellow, light_gray)
    elif (ball_position == 5):   
        cube3.set_light_corners(light_yellow, light_off, light_blue, light_off)
    elif (ball_position == 6):   
        cube3.set_light_corners(light_blue, light_off, light_yellow, light_off)
	
def cozmo_program(_robot: cozmo.robot.Robot):
    # variables globales
    global robot
    global cube1
    global cube2
    global cube3
    global ready
    global ball_direction
    global ball_position
    global ball_speed
    global ready
     
    robot = _robot
    # Les cubes représentent le terrain de jeu
    cube1 = robot.world.get_light_cube(LightCube1Id)
    cube2 = robot.world.get_light_cube(LightCube2Id)
    cube3 = robot.world.get_light_cube(LightCube3Id)

    # introduction
    robot.play_anim_trigger(cozmo.anim.Triggers.BouncerIdeaToPlay).wait_for_completed()
    robot.say_text("Salut").wait_for_completed()
    robot.say_text("Voici le jeu du tennis.").wait_for_completed()
    robot.say_text("Assurez vous que les cubes forment un terrain de tennis").wait_for_completed()    
    robot.say_text("La partie rouge du coté du joueur 1").wait_for_completed()    
    robot.say_text("La partie bleu du coté du joueur 2").wait_for_completed()    
    i=0
    while (i < 3):
        draw_field_intro()
        i += 1
    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabYes).wait_for_completed()
    robot.say_text("Assurez vous que la balle se déplace correctement, d'un côté à l'autre du terrain").wait_for_completed()    
    robot.say_text("Tappez un cube lorsque tout est prêt").wait_for_completed()
    robot.world.add_event_handler(cozmo.objects.EvtObjectTapped, isReady)
    while (ready is False):
        draw_field()
        draw_ball()
        time.sleep(ball_speed)
        if (ball_position == 0):
            ball_direction=1
        elif (ball_position == 6):
            ball_direction=-1
        ball_position += ball_direction
    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabYes).wait_for_completed()
			        
    time.sleep(10)
	
cozmo.run_program(cozmo_program, use_viewer=True)
