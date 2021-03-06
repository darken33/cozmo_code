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
scj1 = 0
scj2 = 0
service = 1

def isReady(evt, *, obj, tap_count, tap_duration, tap_intensity, **kwargs):
    global ready
    ready = True

def cubeTapped(evt, *, obj, tap_count, tap_duration, tap_intensity, **kwargs):
    global ready
    global ball_direction
    global ball_position
    global ball_speed
    global ready
    global service
    global scj1
    global scj2
    # joueur 1
    if (obj.cube_id is LightCube1Id):
        if (ball_direction == -1):
            # Fond de court on ralenti la balle
            if (ball_position == 0):
                ball_direction = 1
                if (ball_speed < 0.5):
                    ball_speed += 0.1
            # Milieu de court 
            elif (ball_position == 1):
                ball_direction = 1
            # Au filet on accélère la balle 
            elif (ball_position == 2):
                ball_direction = 1
                if (ball_speed > 0.1):
                    ball_speed -= 0.1
            else:
                # Frappe au mauvais moment
                scj2 += 1
                service = 1
                ball_position = 0
                ball_direction = 1
                ball_speed = 0.5
                ready = True	    
        else:
            # Frappe au mauvais moment
            scj2 += 1
            service = 1
            ball_position = 0
            ball_direction = 1
            ball_speed = 0.5
            ready = True	    
    # joueur 2
    elif (obj.cube_id is LightCube3Id):
        if (ball_direction == 1):
            # Fond de court on ralenti la balle
            if (ball_position == 6):
                ball_direction = -1
                if (ball_speed < 0.5):
                    ball_speed += 0.1
            # Milieu de court 
            elif (ball_position == 5):
                ball_direction = -1
            # Au filet on accélère la balle 
            elif (ball_position == 4):
                ball_direction = -1
                if (ball_speed > 0.1):
                    ball_speed -= 0.1
            else:
                # Frappe au mauvais moment
                scj1 += 1
                service = 2
                ball_position = 6
                ball_direction = -1
                ball_speed = 0.5
                ready = True	    
        else:
            # Frappe au mauvais moment
            scj1 += 1
            service = 2
            ball_position = 6
            ball_direction = -1
            ball_speed = 0.5
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
    time.sleep(0.5)	
    cube1.set_light_corners(light_red, light_off, light_off, light_off)
    time.sleep(0.5)	
    cube1.set_light_corners(light_red, light_off, light_red, light_off)
    time.sleep(0.5)	
    cube2.set_light_corners(light_red, light_off, light_off, light_off)
    time.sleep(0.5)	
    cube2.set_light_corners(light_red, light_gray, light_off, light_gray)
    time.sleep(0.5)	
    cube2.set_light_corners(light_red, light_gray, light_blue, light_gray)
    time.sleep(0.5)	
    cube3.set_light_corners(light_blue, light_off, light_off, light_off)
    time.sleep(0.5)	
    cube3.set_light_corners(light_blue, light_off, light_blue, light_off)
    time.sleep(0.5)	

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
    global service
    global scj1
    global scj2
     
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
    robot.world.remove_event_handler(cozmo.objects.EvtObjectTapped, isReady)
    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabYes).wait_for_completed()
     
    # boucle de jeu
    service = 1
    ball_position = 0
    ball_direction = 1
    while (scj1<5 and scj2<5):
        # Attendre le service
        ready = False
        if (service == 1):
            ball_position = 0
        else:
            ball_position = 6	
        while (ready is False):
            draw_field()
            draw_ball()
            target = robot.world.wait_for(cozmo.objects.EvtObjectTapped)
            if ((target.obj.cube_id is LightCube1Id and service == 1) or (target.obj.cube_id is LightCube3Id and service == 2)):
                ready = True
        # Echange
        ready = False
        robot.world.add_event_handler(cozmo.objects.EvtObjectTapped, cubeTapped)
        while (ready is False):
            draw_field()
            draw_ball()
            time.sleep(ball_speed)
            ball_position += ball_direction
            if (ball_position < 0):
                scj2 += 1
                service = 1
                ball_position = 0
                ball_direction = 1
                ball_speed = 0.5
                ready = True
            elif (ball_position > 6):
                scj1 += 1
                service = 2
                ball_position = 6
                ball_direction = -1
                ball_speed = 0.5
                ready = True
        # un point a été marqué
        robot.world.remove_event_handler(cozmo.objects.EvtObjectTapped, cubeTapped)
        robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabYes).wait_for_completed()
        robot.say_text(str(scj1) + " à " + str(scj2)).wait_for_completed()    
    
    # Fin de partie			
    if (scj1 >= 5):
        robot.say_text("Vainqueur joueur 1 !").wait_for_completed()    
    else:
        robot.say_text("Vainqueur joueur 2 !").wait_for_completed()    
    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabWin).wait_for_completed()
    time.sleep(1)
	
cozmo.run_program(cozmo_program, use_viewer=True)
