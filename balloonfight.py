import pgzrun
import pygame
import pgzero
from pgzero.builtins import Actor
import os,sys
from random import randint
import pandas as pd
from openpyxl import Workbook
import xlsxwriter


# score = int(input("What is your Score?"))
#
# read_xl = pd.read_excel('high-scores.xlsx',header=0)
# data = {
#     'Score': [score]
# }
# df = pd.DataFrame(data)
#
#
# df.to_excel('high-scores.xlsx',startrow=,index=False,header=False)
# read_xl.nlargest(8,"Scores")
#
#
#
# # wb = Workbook()
# # ws = wb.active
# # Name_array = ("A"+ str(new_line))
# # ws[Name_array] = score
# # # ws.append([score])
# # wb.save("high-scores.xlsx")
#
# print("Test")
# print("Test")
import time
import math

WIDTH = 800
HEIGHT = 600
balloon = Actor("balloon")
balloon.pos = 400, 300
bird = Actor("bird-up")
bird.pos = randint(800, 1600), randint(10, 200)
missile = Actor("missile")
missile.pos = randint(800, 1600), randint(10, 200)
house = Actor("house")
house.pos = randint(800, 1600), 460
tree = Actor("tree")
tree.pos = randint(800, 1600), 450
bird_up = True
up = False
game_over = False
score = 0
number_of_updates = 0
scores = []
lives = 3
multiplier = 0

# def lvl_of_difficulty():
#     global multiplier
#     multiplier = math.floor(score / 10)



def update_high_scores():
    global score, scores
    filename = r"/Users/Nasco/PycharmProjects/Lab8/high-scores.txt"
    scores = []
    with open(filename, "r") as file:
        line = file.readline()
        high_scores = line.split()
        for high_score in high_scores:
            if(score > int(high_score)):
                scores.append(str(score) + " ")
                score = int(high_score)
        else:
            scores.append(str(high_score) + " ")
    with open(filename, "w") as file:
        for high_score in scores:
            file.write(high_score)

def display_high_scores():
    screen.draw.text("HIGH SCORES", (350, 150), color="black")
    y = 175
    position = 1
    for high_score in scores:
        screen.draw.text(str(position) + ". " + high_score, (350, y), color="black")
        y += 25
        position += 1

def draw():
    screen.blit("background", (0, 0))
    if not game_over:
        balloon.draw()
        bird.draw()
        missile.draw()
        house.draw()
        tree.draw()
        screen.draw.text("Score: " + str(score), (700, 5), color="black")
        screen.draw.text("Level: " + str(multiplier), (500, 5), color="black")
        screen.draw.text("Lives: " + str(lives), (300, 5), color="black")
    else:
        display_high_scores()

def on_mouse_down():
    global up
    up = True
    balloon.y -= 50

def on_mouse_up():
    global up
    up = False

def flap():
    global bird_up
    if bird_up:
        bird.image = "bird-down"
        bird_up = False
    else:
        bird.image = "bird-up"
        bird_up = True

def update():
    global game_over, score, number_of_updates,lives, multiplier
    if not game_over:
        multiplier = math.ceil(score / 10)
        if not up:
            balloon.y += 1
        else:
            pass
        if missile.x > 0:
            missile.x -= 8 * multiplier
        else:
            number_of_updates += 1

        if number_of_updates == 9:
            flap()
            number_of_updates = 0
        else:
            number_of_updates += 1
        if bird.x > 0:
            bird.x -= 4 * multiplier
        else:
            bird.x = randint(800, 1600)
            bird.y = randint(10, 200)
            missile.x = randint(800, 1600)
            missile.y = randint(200, 400)
            score += 1
            number_of_updates = 0
        if house.right > 0:
            house.x -= 2 * multiplier
        else:
            house.x = randint(800, 1600)
            score += 1
        if tree.right > 0:
            tree.x -= 4
        else:
            tree.x = randint(800, 1600)
            score += 1
        if balloon.top < 0 :
            lives -= 1
            balloon.y += 125
        elif balloon.bottom > 560:
            lives -= 1
            balloon.y -= 125
        if balloon.collidepoint(bird.x, bird.y) or \
            balloon.collidepoint(house.x, house.y) or \
            balloon.collidepoint(missile.x, missile.y) or \
                balloon.collidepoint(tree.x, tree.y):
                lives -= 1
        elif lives <= 0:
            game_over = True
            update_high_scores()
pgzrun.go()