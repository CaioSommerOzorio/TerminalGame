import time
import os
import socket
import keyboard as kb

# use same host and port, that used on server side.
host = "10.0.0.8"
port = 8080

# creating socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((host, port))

with open("map/map.ans", "r") as file:
    og_map = file.readlines()
with open("map/map.ans", "r+") as file:
    main_map = file.readlines()
with open("icons/frame.txt", "r") as file:
    frame = file.readlines()

# Make game grid
cols, rows = 120, 36
game_console = [[" "] * cols for _ in range(rows)]

def replacer(string, replace, index):
    newstr = ""
    for i in range(1, index):
        newstr+=string[i]
    newstr+=replace
    for i in range(index+1, len(string)):
        newstr+=string[i]

# Prints out img in any part of the console
def draw(img, x, y):
    for i in range(len(img)):
        for j in range(len(img[i])):
            if img[i][j] != "\n":
                game_console[i+y][j+x] = str(img[i][j])

# Same as draw but adds text instead, singular loop because it's a string not a list of strings
def write(text, x, y):
    for i in range(len(text)):
        game_console[y][x+i] = text[i]

def refresh():
    os.system("cls")
    for i in range(rows):
        for j in range(cols):
            print(game_console[i][j], end="")
        print()

def walk(main_map_data, playerx, playery):
    for i in range(1, 35):
        for j in range(1, 118):
            game_console[i][j] = main_map_data[i+playery][j+playerx]
    write("@", 60, 18)
    to_refresh = True
    

def remove_first_char(string):
    newstring = ""
    for i in range(1, len(string)):
        newstring.join(string[i])

def colorize():
    for i in range(36):
        for j in range(120):
            if game_console[i][j] == "#":
                game_console[i][j] = "\033[38;5;21m#"
            elif game_console[i][j] == "^":
                game_console[i][j] = "\033[38;5;10m^"
            elif game_console[i][j] == "[":
                game_console[i][j] = "\033[38;5;10m["
            elif game_console[i][j] == "]":
                game_console[i][j] = "\033[38;5;10m]"
            elif game_console[i][j] == "H":
                game_console[i][j] = "\033[38;5;8mH"
            elif game_console[i][j] == "8":
                game_console[i][j] = "\033[38;5;94m8"
            elif game_console[i][j] == "<":
                game_console[i][j] = "\033[38;5;10m<"
            elif game_console[i][j] == ">":
                game_console[i][j] = "\033[38;5;10m>"
            elif game_console[i][j] == "=":
                game_console[i][j] = "\033[38;5;11m="
            elif game_console[i][j] == "O":
                game_console[i][j] = "\033[38;5;123mO"
            elif game_console[i][j] == "_":
                game_console[i][j] = "\033[38;5;10m_"
            elif game_console[i][j] == ":":
                game_console[i][j] = "\033[38;5;142m:"
            elif game_console[i][j] == "|":
                game_console[i][j] = "\033[38;5;94m|"
            elif game_console[i][j] == "/":
                game_console[i][j] = "\033[38;5;94m/"
            elif game_console[i][j] == "\\":
                game_console[i][j] = "\033[38;5;94m\\"
            elif game_console[i][j] == "+":
                game_console[i][j] = "\033[38;5;1m+"
            else:
                game_console[i][j] = "\033[38;5;255m"+game_console[i][j]

name = input("Enter name: ")
to_refresh = False
prev_coors = ""
blocked_chars = "/|[]\\_H#"
character_x = 170
character_y = 80
draw(frame, 0, 0)
oldcoors = []
while True:
    if kb.is_pressed('up'):
        if main_map[character_y-1+18][character_x+60] not in blocked_chars:
            character_y-=1
            to_refresh = True
    elif kb.is_pressed("down"):
        if main_map[character_y+1+18][character_x+60] not in blocked_chars:
            character_y+=1
            to_refresh = True
    elif kb.is_pressed("left"):
        if main_map[character_y+18][character_x-1+60] not in blocked_chars:
            character_x-=1
            to_refresh = True
    elif kb.is_pressed("right"):
        if main_map[character_y+18][character_x+1+60] not in blocked_chars:
            character_x+=1
            to_refresh = True
    #print("changed player x and y")
    walk(main_map, character_x, character_y)
    #print("walked")
    time.sleep(0.1)
    sock.send(str.encode(f"{name} {character_x} {character_y}"))
    #print("sent character name and coordinates")
    message = sock.recv(1024).decode()
    #print("message received and decoded")
    newcoors = message.split(' ')
    #print(newcoors)
    #print("message splitted")
    if len(newcoors) == 3 and newcoors[0] != name:
        # check if in bounds
        bounds = [character_x+120, character_y+35]
        #print(bounds)
        if (int(newcoors[1]) < bounds[0] and int(newcoors[1]) > character_x-60) and (int(newcoors[2]) < bounds[1] and int(newcoors[2]) >= character_y-18):
            player_x = int(newcoors[1])
            player_y = int(newcoors[2])
            #print(player_x-character_x+60)
            #print(player_y-character_y+18)
            write("L", player_x-character_x+60, player_y-character_y+18)
            if newcoors != oldcoors:
                to_refresh = True
            #print("                               player x      player x       player y      player y")
            #print(f"out of bounds, condition failed: ({int(newcoors[1])} < {bounds[0]} and {int(newcoors[1])} > {character_x-60}) and ({int(newcoors[2])} < {bounds[1]} and {int(newcoors[2])} >= {character_y-18})")
            #print("                                     self x+120     self x         self y+35        self y")
        #print("name was itself")
        #print(newcoors)
    write(str(character_x)+"  ", 93, 27)
    write(str(character_y)+"  ", 93, 29)
    colorize()
    #print("draw and colorized!")
    if to_refresh == True:
        refresh()
        to_refresh = False
    oldcoors = newcoors
