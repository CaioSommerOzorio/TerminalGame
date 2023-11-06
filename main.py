import keyboard as kb
import time
import os
from colorama import init, Fore, Back

init()

# make game grid
cols, rows = 120, 36
game_console = [[""] * cols for _ in range(rows)]

def refresh():
    os.system("cls")
    print("\n\n")
    for i in range(rows):
        for j in range(cols):
            print(game_console[i][j], end="")
        print()

def game_over():
    pass


def change_health(current_health, x, y):
    health = int(current_health)
    if health <= 0:
        game_over()
    health = str(pad(health))
    game_console[y+1][x+2] = health[0]
    game_console[y+1][x+3] = health[1]
    game_console[y+1][x+4] = health[2]

# 25 -> 025
def pad(num):
    num = str(num)
    if len(num) == 2:
        num = "0" + num
        return int(num)
    if len(num) == 1:
        num = "00" + num
        return int(num)
    return int(num)

# declare file icons

health_bar = open("health_bar.txt", "r").readlines()
frame = open("frame.txt", "r").readlines()
sep = open("options.txt", "r").readlines()
boss = open("boss.txt", "r").readlines()
heal_icon = open("heal.txt", "r").readlines()
attack_icon = open("attack.txt", "r").readlines()
player_icon = open("player.txt", "r").readlines()
sword_icon = open("sword.txt", "r").readlines()
apple_icon = open("apple.txt", "r").readlines()

apple = {
    "type": "item",
    "effect": "heal",
    "effect_quantity": 15,
    "name": "Apple"
}

wooden_sword = {
    "type": "weapon",
    "effect": ["slash"],
    "effect_quantity": 30,
    "name": "Wooden sword"
}

def add_img(img, x, y):
    for i in range(len(img)):
        for j in range(len(img[i])):
            if img[i][j] != "\n":
                #print("iteration:", i, j)
                game_console[i+y][j+x] = img[i][j]

def add_text(text, x, y):
    for i in range(len(text)):
        game_console[y][x+i] = text[i]

add_img(frame, 0, 0)
add_img(sep, 0, 25)
add_img(health_bar, 56, 24)
add_img(boss, 30, 4)
add_img(heal_icon, 10, 28)
add_img(attack_icon, 43, 28)
add_img(player_icon, 106, 26)
add_img(sword_icon, 95, 27)
add_img(apple_icon, 80, 26)
add_text(f"{wooden_sword['name']}", 88, 33)
add_text(f"{apple['name']}", 86, 34)
change_health(100, 56, 24)
refresh()

"""
while True:
    if kb.is_pressed("a") == True:
        time.sleep(0.2)
        print("You pressed a!")
        break"""