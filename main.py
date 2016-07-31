#starts up pygame
import pygame
import sys
import random
#import pdb

pygame.init()

screen = pygame.display.set_mode((500, 600))
pygame.event.set_allowed(None)
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN])
pygame.font.init()

log = pygame.font.SysFont("monospace", 15)
big = pygame.font.SysFont("monospace", 50)
text = [log.render("", True, pygame.Color("black")) for i in range(5)] #for the updatelog function

#loads graphics
wall = pygame.image.load('graphics/wall.png').convert()
statue = pygame.image.load('graphics/statue.png').convert()
ground = pygame.image.load('graphics/ground.png').convert()
upstair = pygame.image.load('graphics/upstair.png').convert()
downstair = pygame.image.load('graphics/downstair.png').convert()
player = pygame.image.load('graphics/player.png').convert()
goblin = pygame.image.load('graphics/goblin.png').convert()
rat = pygame.image.load('graphics/rat.png').convert()
treasure = pygame.image.load('graphics/treasure.png').convert()
bag = pygame.image.load('graphics/bag.png').convert()
key = pygame.image.load('graphics/key.png').convert()
keyinv = pygame.image.load('graphics/keyinv.png').convert()
door = pygame.image.load('graphics/door.png').convert()

#creates player variables
plhp = 10
maxhp = 10
weapon = "fist"
level = 1
xp = 0
nextlvl = [0 for i in range(50)]
nextlvl[1] = 10
for i in range(2, 50):
    nextlvl[i] = nextlvl[i - 1] * 1.25 + 1
    nextlvl[i] = int(nextlvl[i])
platt = 1
armor = 10
invmax = -1
haskey = False

#loads map from text file
mapfile = open('rooms/fl1r8.txt', 'r')
floor, room = 1, 8
downstrpos = (0, 0)
upstrpos = (0, 0)
keypos = (0, 0)
dooropen = [(0, 0)]
keyused = [(0, 0)]
map1D = mapfile.read()
map1D = map1D.replace('\n', '')
backmap = [[0 for i in range(10)] for j in range(10)] #creates an empty 2D array
foremap = [[0 for i in range(10)] for j in range(10)]
screen.blit(log.render("HP: " + str(plhp) + "/" + str(maxhp), True, pygame.Color("white")), (50, 500))
screen.blit(log.render("XP: " + str(xp) + "/" + str(nextlvl[level]), True, pygame.Color("white")), (150, 500))

#spilts the 1D array into 2D
for i in range(10):
    for j in range(10):
        backmap[i][j] = map1D[i * 10 + j]

#assigns the graphics to the text
for i in range(10):
    for j in range(10):
        if backmap[i][j] == '#':
            foremap[i][j] = wall
            backmap[i][j] = wall
        if backmap[i][j] == '.':
            foremap[i][j] = ground
            backmap[i][j] = ground
        if backmap[i][j] == '@':
            plx, ply = i, j
            foremap[i][j] = player
            backmap[i][j] = ground
        if backmap[i][j] == 'D':
            foremap[i][j] = door
            backmap[i][j] = ground

#puts the graphics on the screen
for i in range(10):
    for j in range(10):
        screen.blit(foremap[i][j], (j * 50, i * 50))
pygame.display.update()

def updatelog(kind, thing = 0, value = 0):
    global text
    text[4] = text[3]
    text[3] = text[2]
    text[2] = text[1]
    text[1] = text[0]
    newlog = pygame.Rect(0, 585, 600, 15)
    thing = str(thing)
    value = str(value)

    screen.fill(pygame.Color("black"), (0, 515, 600, 85))
    screen.blit(text[4], newlog.move(0, -60))
    screen.blit(text[3], newlog.move(0, -45))
    screen.blit(text[2], newlog.move(0, -30))
    screen.blit(text[1], newlog.move(0, -15))

    if kind == 'view':
        text[0] = log.render("You see a " + thing, True, pygame.Color("white"))
    if kind == 'att':
        text[0] = log.render("You deal " + value + " damage to the " + thing, True, pygame.Color("blue"))
    if kind == 'miss':
        text[0] = log.render("You miss the " + thing, True, pygame.Color("white"))
    if kind == 'dam':
        text[0] = log.render("The " + thing + " hits you for " + value + " damage", True, pygame.Color("red"))
    if kind == 'pick':
        text[0] = log.render("You Pick up the " + thing, True, pygame.Color("white"))
    if kind == 'heal':
        text[0] = log.render("You healed yourself for " + value + " damage", True, pygame.Color("yellow"))
    if kind == 'level':
        text[0] = log.render("You are now level " + thing, True, pygame.Color("blue"))
    if kind == 'stat':
        text[0] = log.render("Your " + thing + " stat went up by " + value, True, pygame.Color("blue"))
    if kind == 'dead':
        text[0] = log.render("You died", True, pygame.Color("red"))
    
    screen.blit(text[0], newlog)

def levelup(lvlxp):
    global xp, maxhp, platt, armor
    if xp >= lvlxp:
        rn = random.randint(0, 2)
        rnstat = 0
        cursor = 0
        updatelog('level', level + 1)
        stats = ["HP", "Attack", "Defence"]

        screen.fill(pygame.Color("black"), (0, 515, 600, 85))
        for i in range(len(stats)):
            screen.blit(log.render(stats[i], True, pygame.Color("white")), (30, 525 + i * 20))
        screen.blit(log.render("_______", True, pygame.Color("white")), (30, 528))
        pygame.display.update()

        done = False
        while not done:
            select = pygame.event.wait()
            screen.fill(pygame.Color("black"), (29, (cursor * 20) + 540, 150, 5))
            if select.type == pygame.QUIT:
                sys.exit()
            elif select.type == pygame.KEYDOWN:
                if select.key == pygame.K_DOWN and cursor + 1 != 3:
                    cursor += 1
                if select.key == pygame.K_UP and cursor - 1 != -1:
                    cursor -= 1
                if select.key == pygame.K_RETURN:
                    choice = stats[cursor]
                    done = True
            screen.blit(log.render("_______", True, pygame.Color("white")), (30, (cursor * 20) + 528))
            pygame.display.update()

        if choice == "HP":
            rnstat = random.randint(5, 10)
            updatelog('stat', "HP", rnstat)
            maxhp += rnstat
            
            screen.fill(pygame.Color("black"), (115, 500, 23, 15))
            screen.blit(log.render(str(maxhp), True, pygame.Color("white")), (115, 500))
        if choice == "Attack":
            rnstat = random.randint(1, 3)
            updatelog('stat', "attack", rnstat)
            platt += rnstat
        if choice == "Defence":
            rnstat = random.randint(1, 3)
            updatelog('stat', "defence", rnstat)
            armor += rnstat

        xp = 0
        return level + 1
    else:
        return level 

class Item():
    pos = (0, 0)
    curs = -1
    used = [(0, 0)]
    equip = False
    ininv = False
    def __init__(self, name, kind, value, image, damage = 0, rmfl = 0): #the rmfl is only for treasure and damage is for weapons
        self.name = name
        self.kind = kind
        self.value = value
        self.image = image
        self.damage = damage
        self.rmfl = rmfl

    def use(self):
        global weapon, plhp, maxhp, invmax
        if self.kind == 'WEAP':
            if self.equip == False:
                self.equip = True
                weapon = self
            else:
                self.equip = False
                weapon = "fist"
        if self.kind == 'HEAL' and self.ininv == True:
            if self.value + plhp > maxhp:
                plhp = maxhp
            else:
                plhp += self.value
            self.ininv = False
            invmax -= 1
            self.used.append(self.rmfl)
            screen.fill(pygame.Color("black"), (80, 500, 23, 15))
            screen.blit(log.render(str(plhp), True, pygame.Color("white")), (85, 500))
            

items = [
#---ITEMS GO HERE---#
Item("Sword", 'WEAP', 5, treasure, 8, (5, 1)),
Item("Potion", 'HEAL', 5, bag),
Item("Potion", 'HEAL', 5, bag),
Item("Potion", 'HEAL', 5, bag),
Item("Potion", 'HEAL', 5, bag),
Item("Potion", 'HEAL', 5, bag),
Item("Potion", 'HEAL', 5, bag),
Item("Potion", 'HEAL', 5, bag),
Item("Potion", 'HEAL', 5, bag),
Item("Potion", 'HEAL', 5, bag)
#---ITEMS END HERE---#
]

#the enemy class    I don't even know
class Enemy():
    enx, eny = 0, 0
    loaded = False
    dead = False
    keepgo = 'UP'
    rmfl = (0, 0)
    used = [(0, 0)]
    def __init__(self, name, hp, att, armor, xp, image):
        self.name = name
        self.hp = hp
        self.temphp = hp
        self.att = att
        self.armor = armor
        self.xp = xp
        self.image = image

    def los(self):
        x = self.enx
        y = self.eny
        if plx > x or ply > y:
            while foremap[x + 1][y] != wall and x != plx:
                if x + 2 <= len(foremap) - 1:
                    x += 1
                else:
                    return False
            while foremap[x][y + 1] != wall and y != ply:
                if y + 2 <= len(foremap) - 1:
                    y += 1
                else:
                    return False
        if plx < x or ply < y:
            while foremap[x - 1][y] != wall and x != plx:
                x -= 1
            while foremap[x][y - 1] != wall and y != ply:
                y -= 1
        if (x, y) == (plx, ply):
            return True
        else:
            return False

    def enatt(self, hp):
        if self.loaded == True:
            rn = random.randint(0, 2)
            updatelog('dam', self.name, self.att + rn)
            return hp - (self.att + rn)

    def enmv(self, direct): #at least it works
        global foremap, plhp
        pos = foremap[self.enx][self.eny]
        down = foremap[self.enx + 1][self.eny]
        up = foremap[self.enx - 1][self.eny]
        right = foremap[self.enx][self.eny + 1]
        left = foremap[self.enx][self.eny - 1]
        rn = random.randint(0, 1)
        attacked = False

        if rn == 0:
            leri = 'LEFT'
            updo = 'UP'
        elif rn == 1:
            leri = 'RIGHT'
            updo = 'DOWN'

        if self.loaded == True and attacked == False:
            if down == player or up == player or right == player or left == player:
                plhp = self.enatt(plhp)
                attacked = True
        if self.loaded == True and attacked == False:

            foremap[self.enx][self.eny] = backmap[self.enx][self.eny]

            if self.los() == True:
                if self.enx < plx and down != wall:
                    self.enx += 1
                elif self.enx > plx and up != wall:
                    self.enx -= 1
                elif self.eny < ply and right != wall:
                    self.eny += 1
                elif self.eny > ply and left != wall:
                    self.eny -= 1

            else:
                if direct == 'DOWN':
                    if down != wall:
                        self.enx += 1
                    else:
                        foremap[self.enx][self.eny] = self.image
                        return leri
                elif direct == 'UP':
                    if up != wall:
                        self.enx -= 1
                    else:
                        foremap[self.enx][self.eny] = self.image
                        return leri
                elif direct == 'RIGHT':
                    if right != wall:
                        self.eny += 1
                    else:
                        foremap[self.enx][self.eny] = self.image
                        return updo
                elif direct == 'LEFT':
                    if left != wall:
                        self.eny -= 1
                    else:
                        foremap[self.enx][self.eny] = self.image
                        return updo

            foremap[self.enx][self.eny] = self.image
        return direct

    def die(self):
        global xp
        if self.hp <= 0:
            self.dead = True
            loaded = False
            xp += self.xp
            self.rmfl = (0, 0)

    def recycle(self):
        self.dead = False
        self.hp = self.temphp
            
enemies = [
#---MONSTERS GO HERE---#
Enemy("Goblin", 5, 0, 5, 2, goblin),
Enemy("Goblin", 5, 0, 5, 2, goblin),
Enemy("Goblin", 5, 0, 5, 2, goblin),
Enemy("Goblin", 5, 0, 5, 2, goblin),
Enemy("Goblin", 5, 0, 5, 2, goblin),
Enemy("Rat", 3, 0, 3, 1, rat),
Enemy("Rat", 3, 0, 3, 1, rat),
Enemy("Rat", 3, 0, 3, 1, rat),
Enemy("Rat", 3, 0, 3, 1, rat),
Enemy("Rat", 3, 0, 3, 1, rat)
#---NONSTERS END HERE---#
]

def getmon(x, y):
    temp = False
    
    #gets the monster that was already there
    for i in range(len(enemies)):
        if enemies[i].rmfl == (room, floor) and enemies[i].loaded == False:
            for j in range(len(enemies[i].used)):
                if enemies[i].used[j] == (room, floor):
                    temp1 = True
            if temp == False:
                enemies[i].loaded = True
                enemies[i].enx = x
                enemies[i].eny = y
                if enemies[i].dead == False:
                    updatelog('view', enemies[i].name)
                return enemies[i].image

    #gets a random new monster
    temp = 0
    while True:
        rn = random.randint(0, len(enemies) - 1)
        if enemies[rn].dead == False:
            enemies[rn].enx = x
            enemies[rn].eny = y
            enemies[rn].loaded = True
            enemies[rn].rmfl = (room, floor)
            enemies[rn].used.append(enemies[rn].rmfl)
            updatelog('view', enemies[rn].name)
            return enemies[rn].image
        for i in range(len(enemies)):
            if enemies[i].dead == True:
                temp += 1
            if temp >= len(enemies):
                return ground

def getitem(x, y, kind):
    temp = False

    for i in range(len(items)):
        if items[i].rmfl == (room, floor):
            if kind == 'T' and items[i].image == treasure and items[i].ininv == False:
                items[i].pos = (x, y)
                return items[i].image
            for j in range(len(items[i].used)):
                if items[i].used[j] == (room, floor):   #makes it so an item can never respawn in the same room
                    temp = True
            if kind == 'B' and items[i].image == bag and items[i].ininv == False and temp == False:
                items[i].pos = (x, y)
                return items[i].image
            if items[i].ininv == True or temp == True:
                return ground

    while True:
        rn = random.randint(0, len(items) - 1)
        if items[rn].ininv == False and items[rn].rmfl == 0 and items[rn].image == bag:
            items[rn].rmfl = (room, floor)
            items[rn].pos = (x, y)
            return items[rn].image

def pickup():
    global keypos, haskey, invmax
    if (plx, ply) == keypos:
        haskey = True
        keyused.append((room, floor))
        foremap[plx][ply] = player 
        backmap[plx][ply] = ground
    for i in range(len(items)):
        if items[i].pos == (plx, ply) and items[i].rmfl == (room, floor):
            items[i].ininv = True
            items[i].pos = (0, 0)
            backmap[plx][ply] = ground
            invmax += 1

def openinv():
    cursor = 0
    while True:
        screen.fill(pygame.Color("black"), (0, 0, 500, 500))
        temp = 0
        for i in range(len(items)):
            if items[i].ininv == True:
                screen.blit(log.render(items[i].name + "    " + str(items[i].value), True, pygame.Color("white")), (50, (temp * 50) + 50))
                items[i].curs = temp
                temp += 1
            if items[i].equip == True:
                screen.blit(log.render("*", True, pygame.Color("white")), (40, (items[i].curs * 50) + 50))
        screen.blit(log.render("________", True, pygame.Color("white")), (50, (cursor * 50) + 60))
        pygame.display.update()

        select = pygame.event.wait()
        screen.fill(pygame.Color("black"), (45, (cursor * 50) + 65, 90, 10))
        if select.type == pygame.QUIT:
            sys.exit()
        elif select.type == pygame.KEYDOWN:
            if select.key == pygame.K_UP and cursor - 1 >= 0:
                cursor -= 1
            if select.key == pygame.K_DOWN and cursor + 1 <= invmax:
                cursor += 1
            if select.key == pygame.K_RETURN:
                for i in range(len(items)):
                    if items[i].curs == cursor:
                        items[i].use()
            if select.key == pygame.K_i:
                return
        screen.blit(log.render("________", True, pygame.Color("white")), (50, (cursor * 50) + 60))
        pygame.display.update()

def attack(enemy, weapon):
    rn = random.randint(1, 20) #d20

    if weapon == "fist":
        if rn + platt > enemy.armor:
            dam = random.randint(1, 3)
            updatelog('att', enemy.name, dam)
            return enemy.hp - dam
        else:
            updatelog('miss')
            return enemy.hp

    if rn + weapon.value + platt > enemy.armor:
        dam = random.randint(1, weapon.damage)
        updatelog('att', enemy.name, dam)
        return enemy.hp - dam
    else:
        updatelog('miss')

#load in another map file and display it on the screen
def loadmap(direct):    #TO DO add the R = rat, G = goblin thing
    global foremap, backmap, plx, ply, floor, room, upstrpos, downstrpos, keypos
    upstrpos = (0, 0)
    downstrpos = (0, 0)
    keypos = (0, 0)
    temp = False

    for i in range(len(enemies)):
        enemies[i].loaded = False

    if direct == 'UP':
        room -= 3
        plx = 9
    if direct == 'DOWN':
        room += 3
        plx = 0
    if direct == 'LEFT':
        room -= 1
        ply = 9
    if direct == 'RIGHT':
        room += 1
        ply = 0
    if direct == 'STAIR_UP':
        upstrpos = (0, 0)
        floor -= 1
    if direct == 'STAIR_DOWN':
        downstrpos = (0, 0)
        floor += 1

    newmap = "rooms/fl" + str(floor) + "r" + str(room) + ".txt"
    newmap = open(newmap, 'r')
    newmap = newmap.read()
    newmap = newmap.replace('\n' , '')

    for i in range(10):
        for j in range(10):
            backmap[i][j] = newmap[i * 10 + j]

    for i in range(10):
        for j in range(10):
            if backmap[i][j] == '#':
                foremap[i][j] = wall
                backmap[i][j] = wall
            if backmap[i][j] == '.' or backmap[i][j] == '@':
                foremap[i][j] = ground
                backmap[i][j] = ground
            if backmap[i][j] == '%':
                foremap[i][j] = statue
                backmap[i][j] = statue
            if backmap[i][j] == 'E':
                foremap[i][j] = getmon(i, j)
                backmap[i][j] = ground
            if backmap[i][j] == 'K':
                for k in range(len(keyused)):
                    if keyused[k] == (room, floor):
                        temp = True
                if temp == False:
                    foremap[i][j] = key
                    backmap[i][j] = key
                    keypos = (i, j)
                else:
                    foremap[i][j] = ground
                    backmap[i][j] = ground
            if backmap[i][j] == 'D':
                for k in range(len(dooropen)):
                    if dooropen[k] != (room, floor):
                        foremap[i][j] = door
                    else:
                        foremap[i][j] = ground
                backmap[i][j] = ground
            if backmap[i][j] == 'T':
                foremap[i][j] = getitem(i, j, 'T')
                backmap[i][j] = foremap[i][j]
            if backmap[i][j] == 'B':
                foremap[i][j] = getitem(i, j, 'B')
                backmap[i][j] = foremap[i][j]
            if backmap[i][j] == '<':
                foremap[i][j] = upstair
                backmap[i][j] = upstair
                upstrpos = (i, j)
            if backmap[i][j] == '>':
                foremap[i][j] = downstair
                backmap[i][j] = downstair
                downstrpos = (i, j)

#the move function, you dingus
#it's messy, I know
def move(x):
    global foremap, plx, ply, haskey, dooropen
    load = False #needed because I can't put elifs here
    attacked = False
    foremap[plx][ply] = backmap[plx][ply]
    if x == 'UP':
        if plx == 0:
            loadmap('UP')
            load = True

        for i in range(len(enemies)):
            if plx - 1 == enemies[i].enx and ply == enemies[i].eny and foremap[plx - 1][ply] == enemies[i].image and load == False:
                enemies[i].hp = attack(enemies[i], weapon)
                attacked = True

        if foremap[plx - 1][ply] == door and haskey == True:
            foremap[plx - 1][ply] = backmap[plx - 1][ply]
            haskey = False
            dooropen.append((room, floor))

        elif foremap[plx - 1][ply] != wall and foremap[plx - 1][ply] != statue and foremap[plx - 1][ply] != door and load == False and attacked == False:
            plx -= 1

    if x == 'DOWN':
        if plx == 9:
            loadmap('DOWN')
            load = True

        for i in range(len(enemies)):
           if plx + 1 == enemies[i].enx and ply == enemies[i].eny and foremap[plx + 1][ply] == enemies[i].image and load == False:
                enemies[i].hp = attack(enemies[i], weapon)
                attacked = True

        if foremap[plx + 1][ply] != wall and foremap[plx + 1][ply] != statue and load == False and attacked == False:
            plx += 1

    if x == 'LEFT':
        if ply == 0:
            loadmap('LEFT')
            load = True

        for i in range(len(enemies)):
           if plx == enemies[i].enx and ply - 1 == enemies[i].eny and foremap[plx][ply - 1] == enemies[i].image and load == False:
                enemies[i].hp = attack(enemies[i], weapon)
                attacked = True

        if foremap[plx][ply - 1] != wall and foremap[plx][ply - 1] != statue and load == False and attacked == False:
            ply -= 1

    if x == 'RIGHT':
        if ply == 9:
            loadmap('RIGHT')
            load = True

        for i in range(len(enemies)):
          if plx == enemies[i].enx and ply + 1 == enemies[i].eny and foremap[plx][ply + 1] == enemies[i].image and load == False:
                enemies[i].hp = attack(enemies[i], weapon)
                attacked = True

        if foremap[plx][ply + 1] != wall and foremap[plx][ply + 1] != statue and load == False and attacked == False:
            ply += 1

    if x == 'STAIR_UP':
        if (plx, ply) == upstrpos:
            loadmap('STAIR_UP')

    if x == 'STAIR_DOWN':
        if (plx, ply) == downstrpos:
            loadmap('STAIR_DOWN')

    foremap[plx][ply] = player

#main game loop
while True:
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        sys.exit()
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            move('UP')
        if event.key == pygame.K_DOWN:
            move('DOWN')
        if event.key == pygame.K_LEFT:
            move('LEFT')
        if event.key == pygame.K_RIGHT:
            move('RIGHT')
        if event.key == pygame.K_COMMA and pygame.key.get_mods() & pygame.KMOD_SHIFT:
            move('STAIR_UP')
        if event.key == pygame.K_PERIOD and pygame.key.get_mods() & pygame.KMOD_SHIFT:
            move('STAIR_DOWN')
        if event.key == pygame.K_i:
            openinv()
        if event.key == pygame.K_COMMA:
            pickup()
        if event.key == pygame.K_a:
            xp += 1

    for i in range(len(enemies)):
        enemies[i].die()
        if enemies[i].dead == False:
            tempgo = enemies[i].keepgo
            enemies[i].keepgo = enemies[i].enmv(tempgo)
        else:
            foremap[enemies[i].enx][enemies[i].eny] = backmap[enemies[i].enx][enemies[i].eny]
            enemies[i].enx, enemies[i].eny = 0, 0
            enemies[i].recycle()

    foremap[plx][ply] = player #makes it so you don't go invisible on a tile a monster died on
    foremap[0][0] = wall

    screen.fill(pygame.Color("black"), (80, 500, 23, 15))
    screen.fill(pygame.Color("black"), (150, 500, 100, 15))
    screen.blit(log.render(str(plhp), True, pygame.Color("white")), (86, 500)) #the weird number is used just to keep the value in the same place
    screen.blit(log.render("XP: " + str(xp) + "/" + str(nextlvl[level]), True, pygame.Color("white")), (150, 500))
    if haskey == True:
        screen.blit(keyinv, (350, 500))
    else:
        screen.fill(pygame.Color("black"), (350, 500, 50, 50))

    if plhp <= 0:
        updatelog('dead')
        screen.fill(pygame.Color("black"), (0, 0, 500, 500))
        screen.blit(big.render("GAME OVER", True, pygame.Color("red")), (125, 200))
        pygame.display.update()
        pygame.time.wait(1000)
        event = pygame.event.wait()
        sys.exit()

    for i in range(10):
        for j in range(10):
            screen.blit(foremap[i][j], (j * 50, i * 50))
    pygame.display.update()
    level = levelup(nextlvl[level])
