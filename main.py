import pygame
import sys
import random
import pdb

pygame.init()

screen = pygame.display.set_mode((500, 600))
pygame.event.set_allowed(None)
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN])
pygame.font.init()

log = pygame.font.SysFont("monospace", 15)
big = pygame.font.SysFont("monospace", 50)
text = [log.render("", True, pygame.Color("black")) for i in range(5)] #for the updatelog function

debug = False

#Title Screen
title = big.render("PyRogue", True, pygame.Color("green"))
options = [
log.render("Start Game", True, pygame.Color("white")),
log.render("Debug", True, pygame.Color("white"))
]
screen.blit(title, (150, 150))
for i in range(len(options)):
    screen.blit(options[i], (150, 250 + (i * 25)))
screen.blit(log.render(">", True, pygame.Color("white")), (140, 250))
pygame.display.update()
cursor = 0
loop = True
while loop:
    choice = pygame.event.wait()
    screen.fill(pygame.Color("black"), (135, 245, 15, 100))
    if choice.type == pygame.QUIT:
        sys.exit()
    elif choice.type == pygame.KEYDOWN:
        if choice.key == pygame.K_UP:
            if cursor - 1 >= 0:
                cursor -= 1
        if choice.key == pygame.K_DOWN:
            if cursor + 1 <= len(options) - 1:
                cursor += 1
        if choice.key == pygame.K_RETURN:
            if cursor == 0:
                loop = False
            if cursor == 1:
                debug = True
                loop = False
    screen.blit(log.render(">", True, pygame.Color("white")), (140, 250 + (cursor * 25)))
    pygame.display.update()

#loads graphics
wall = pygame.image.load('graphics/wall.png').convert()
statue = pygame.image.load('graphics/statue.png').convert()
ground = pygame.image.load('graphics/ground.png').convert()
upstair = pygame.image.load('graphics/upstair.png').convert()
downstair = pygame.image.load('graphics/downstair.png').convert()
player = pygame.image.load('graphics/player.png').convert()
goblin = pygame.image.load('graphics/goblin.png').convert()
rat = pygame.image.load('graphics/rat.png').convert()
snake = pygame.image.load('graphics/snake.png').convert()
troll = pygame.image.load('graphics/troll.png').convert()
guinea = pygame.image.load('graphics/guinea.png').convert()
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
psn = False
para = False
paracount = 0
paramax = 0
psnstep = 0
speed = False
speedturn = 0
speedcount = 0
nodam = False
nodamcount = 0
armoron = False
nextlvl = [0 for i in range(50)]
nextlvl[1] = 10
for i in range(2, 50):
    nextlvl[i] = nextlvl[i - 1] * 1.25 + 1
    nextlvl[i] = int(nextlvl[i])
platt = 1
armor = 10
invmax = -1
itemrmflxy = [((0, 0), (0, 0))]
haskey = False

if debug == True:
    plhp = 9999
    maxhp = 9999
    platt = 9999
    armor = 9999

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
    if kind == 'nodam':
        text[0] = log.render("The " + thing + " hits you but you don't take any damage", True, pygame.Color("white"))
    if kind == 'pick':
        text[0] = log.render("You pick up the " + thing, True, pygame.Color("white"))
    if kind == 'heal':
        text[0] = log.render("You healed yourself for " + value + " damage", True, pygame.Color("yellow"))
    if kind == 'level':
        text[0] = log.render("You are now level " + thing, True, pygame.Color("green"))
    if kind == 'stat':
        text[0] = log.render("Your " + thing + " stat went up by " + value, True, pygame.Color("green"))
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
    rmfl = (0, 0)
    curs = -1
    listpos = None
    equip = False
    ininv = False
    dropped = False
    def __init__(self, name, kind, value, image, damage = 0): #damage is for weapons
        self.name = name
        self.kind = kind
        self.value = value
        self.image = image
        self.damage = damage

    def drop(self):
        global invmax, foremap
        if self.ininv == True:
            self.ininv = False
            self.dropped = True
            invmax -= 1
            self.pos = (plx, ply)
            self.rmfl = (room, floor)
            if self.image == bag:
                foremap[plx][ply] = bag
                backmap[plx][ply] = bag
            if self.image == treasure:
                foremap[plx][ply] = treasure
                backmap[plx][ply] = treasure

    def useitem(self):
        global invmax, items
        self.ininv = False
        invmax -= 1
        items.pop(self.listpos)

    def use(self):
        global weapon, plhp, maxhp, armor, armoron
        if self.kind == 'WEAP':
            if self.equip == False and weapon == "fist":
                self.equip = True
                weapon = self
            elif self.equip == True:
                self.equip = False
                weapon = "fist"
        if self.kind == 'ARM':
            if self.equip == False and armoron == False:
                self.equip = True
                armoron = True
                armor += self.value
            elif self.equip == True:
                self.equip = False
                armoron = False
                armor -= self.value
        if self.kind == 'HEAL' and self.ininv == True:
            if self.value + plhp > maxhp:
                plhp = maxhp
            else:
                plhp += self.value
            self.useitem()
            screen.fill(pygame.Color("black"), (80, 500, 23, 15))
            screen.blit(log.render(str(plhp), True, pygame.Color("white")), (85, 500))
            return True
        if self.kind == 'PSN' and self.ininv == True:
            global psn
            if psn == True:
                psn = False
                self.useitem()
                return True
        if self.kind == 'PARA' and self.ininv == True:
            global para
            if para == True:
                para = False
                self.useitem()
                return True
        if self.kind == 'SPD' and self.ininv == True:
            global speed
            if speed == False:
                speed = True
                self.useitem()
                return True
        if self.kind == 'INV' and self.ininv == True:
            global nodam
            if nodam == False:
                nodam = True
                self.useitem()
                return True
            

items = [Item("Potion", 'HEAL', 5, bag)]

def additem(itemlist, itemobj):
    itemobj.listpos = len(itemlist)
    return itemlist.append(itemobj)

#the enemy class    This is magic code now. I have forgotten what most of this is and how it works. I just know it works badly.
class Enemy():
    enx, eny = 0, 0
    spawnx, spawny = 0, 0
    drop = 0
    loaded = False
    dead = False
    boss = False
    keepgo = 'UP'
    rmfl = (0, 0)
    currentloc = ((0, 0), (0, 0)) # room, floor, x, y
    diedin = [(0, 0, 0, 0)] # same as ^ but worse and I don't want to change it
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
            while x < 9 and foremap[x + 1][y] != wall and foremap[x + 1][y] != statue and x != plx:
                    x += 1
            while y < 9 and foremap[x][y + 1] != wall  and foremap[x][y + 1] != statue and y != ply:
                    y += 1
        if plx < x or ply < y:
            while x > 0 and foremap[x - 1][y] != wall  and foremap[x - 1][y] != statue and x != plx:
                x -= 1
            while y > 0 and foremap[x][y - 1] != wall  and foremap[x][y - 1] != statue and y != ply:
                y -= 1
        if (x, y) == (plx, ply):
            return True
        else:
            return False

    def enatt(self, hp):
        global psn, para, paramax
        if self.loaded == True and nodam == False:
            rn = random.randint(0, 2)
            rnstatus = random.randint(0, 100)
            updatelog('dam', self.name, self.att + rn)
            if self.name == "Rat":
                if rnstatus <= 10:
                    psn = True
            if self.name == "Snake":
                if rnstatus <= 10:
                    psn = True
                if rnstatus > 10 and rnstatus <= 20:
                    para = True
                    paramax = 3
            return hp - (self.att + rn)
        elif self.loaded == True and nodam == True:
            updatelog('nodam', self.name)

    def enmv(self, direct): #at least it works
        global foremap, plhp
        pos = foremap[self.enx][self.eny]
        if self.enx + 1 < 10:
            down = foremap[self.enx + 1][self.eny]
        else:
            down = foremap[self.enx][self.eny]
        if self.enx - 1 >= 0:
            up = foremap[self.enx - 1][self.eny]
        else:
            up = foremap[self.enx][self.eny]
        if self.eny + 1 < 10:
            right = foremap[self.enx][self.eny + 1]
        else:
            right = foremap[self.enx][self.eny]
        if self.eny - 1 >= 0:
            left = foremap[self.enx][self.eny - 1]
        else:
            left = foremap[self.enx][self.eny]
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
                if self.enx < plx and down == ground or down == bag or down == treasure or down == upstair or down == downstair:
                    self.enx += 1
                elif self.enx > plx and up == ground or up == bag or up == treasure or up == upstair or up == downstair:
                    self.enx -= 1
                elif self.eny < ply and right == ground or right == bag or right == treasure or right == upstair or right == downstair:
                    self.eny += 1
                elif self.eny > ply and left == ground or left == bag or left == treasure or left == upstair or left == downstair:
                    self.eny -= 1

            else:
                if direct == 'DOWN':
                    if down == ground or down == bag or down == treasure or down == upstair or down == downstair:
                        self.enx += 1
                    else:
                        foremap[self.enx][self.eny] = self.image
                        return leri
                elif direct == 'UP':
                    if up == ground or up == bag or up == treasure or up == upstair or up == downstair:
                        self.enx -= 1
                    else:
                        foremap[self.enx][self.eny] = self.image
                        return leri
                elif direct == 'RIGHT':
                    if right == ground or right == bag or right == treasure or right == upstair or right == downstair:
                        self.eny += 1
                    else:
                        foremap[self.enx][self.eny] = self.image
                        return updo
                elif direct == 'LEFT':
                    if left == ground or left == bag or left == treasure or left == upstair or left == downstair:
                        self.eny -= 1
                    else:
                        foremap[self.enx][self.eny] = self.image
                        return updo

            foremap[self.enx][self.eny] = self.image
        return direct

    def forskellyonly(self):
        global foremap, plhp
        if self.enx - 1 == plx or self.enx + 1 plx or self.eny - 1 == plx or self.eny + 1 == ply:
            rn = random.randint(0, 10):
                if rn <= 3:
                    if self.enx - 1 == plx and foremap[self.enx + 1][self.eny] == ground:
                        self.enx += 1
                        keepgo = 'DOWN'
                    if self.enx + 1 == plx and foremap[self.enx - 1][self.eny] == ground:
                        self.enx -= 1
                        keepgo = 'UP'
                    if self.eny - 1 == ply and foremap[self.enx][self.eny + 1] == ground:
                        self.eny += 1
                        keepgo = 'RIGHT'
                    if self.eny + 1 == ply and foremap[self.enx][self.eny - 1] == ground:
                        self.eny -= 1
                        keepgo = 'LEFT'
                else:
                    plhp = self.enatt(plhp)
        else:
            if keepgo == True:
                RUNAWAY
            if far enough away:
                forskellyonlymagic

    def dropitem(self):
        if random.randint(0, 100) <= 12:
            if floor < 5:
                rn = random.randint(0, 100)
                if rn <= 50:
                    return getitem(self.enx, self.eny, 0, "Potion")
                if rn > 50:
                    return getitem(self.enx, self.eny, 0, "Antidote")
            """if floor >= 5 and floor < 10:
                #stuff
            if floor >= 10:
                #stuff"""

    def die(self):
        global xp, foremap
        self.drop = 0
        if self.hp <= 0:
            self.dead = True
            loaded = False
            xp += self.xp
            if backmap[self.enx][self.eny] == ground:
                self.drop = self.dropitem()
            if self.drop == 0 or self.drop == None:
                foremap[self.enx][self.eny] = backmap[self.enx][self.eny]
            self.diedin.append((room, floor, self.spawnx, self.spawny))
            self.rmfl = (0, 0)
            if self.boss == True:
                dooropen.append((room, floor))
                self.hp = 1
                if floor == 5:
                    foremap[4][0] = ground
                    foremap[5][0] = ground
                    foremap[4][9] = ground
                    foremap[5][9] = ground

    def recycle(self, stair = False):
        self.dead = False
        self.hp = self.temphp
        if stair == True:
            self.loaded = False
            self.rmfl = (0, 0)
            self.enx, self.eny = 0, 0
            self.spawnx, self.spawny = 0, 0
            self.currentloc = ((0, 0), (0, 0))
            
#Name, HP, Attack, Armor, XP, image
enemies = [
#---MONSTERS GO HERE---#
Enemy("Goblin", 5, 0, 5, 2, goblin),
Enemy("Goblin", 5, 0, 5, 2, goblin),
Enemy("Goblin", 5, 0, 5, 2, goblin),
Enemy("Goblin", 5, 0, 5, 2, goblin),
Enemy("Goblin", 5, 0, 5, 2, goblin),
Enemy("Goblin", 5, 0, 5, 2, goblin),
Enemy("Goblin", 5, 0, 5, 2, goblin),
Enemy("Goblin", 5, 0, 5, 2, goblin),
Enemy("Goblin", 5, 0, 5, 2, goblin),
Enemy("Goblin", 5, 0, 5, 2, goblin),
Enemy("Rat", 3, 0, 3, 1, rat),
Enemy("Rat", 3, 0, 3, 1, rat),
Enemy("Rat", 3, 0, 3, 1, rat),
Enemy("Rat", 3, 0, 3, 1, rat),
Enemy("Rat", 3, 0, 3, 1, rat),
Enemy("Rat", 3, 0, 3, 1, rat),
Enemy("Rat", 3, 0, 3, 1, rat),
Enemy("Rat", 3, 0, 3, 1, rat),
Enemy("Rat", 3, 0, 3, 1, rat),
Enemy("Rat", 3, 0, 3, 1, rat),
Enemy("Snake", 5, 1, 5, 3, snake),
Enemy("Snake", 5, 1, 5, 3, snake),
Enemy("Snake", 5, 1, 5, 3, snake),
Enemy("Snake", 5, 1, 5, 3, snake),
Enemy("Snake", 5, 1, 5, 3, snake),
Enemy("Snake", 5, 1, 5, 3, snake),
Enemy("Snake", 5, 1, 5, 3, snake),
Enemy("Snake", 5, 1, 5, 3, snake),
Enemy("Snake", 5, 1, 5, 3, snake),
Enemy("Snake", 5, 1, 5, 3, snake),
Enemy("Guinea Pig", 3, 3, 7, 3, guinea),
Enemy("Guinea Pig", 3, 3, 7, 3, guinea),
Enemy("Guinea Pig", 3, 3, 7, 3, guinea),
Enemy("Guinea Pig", 3, 3, 7, 3, guinea),
Enemy("Guinea Pig", 3, 3, 7, 3, guinea),
Enemy("Guinea Pig", 3, 3, 7, 3, guinea),
Enemy("Guinea Pig", 3, 3, 7, 3, guinea),
Enemy("Guinea Pig", 3, 3, 7, 3, guinea),
Enemy("Guinea Pig", 3, 3, 7, 3, guinea),
Enemy("Guinea Pig", 3, 3, 7, 3, guinea)
#---NONSTERS END HERE---#
]

bosses = [
Enemy("Troll", 15, 6, 6, 15, troll)
]
def getrandmon():
    rn = random.randint(1, 100)
    if floor < 3:
        if rn <= 50:
            return 0
        if rn > 50:
            return 10
    if floor >= 3 and floor < 5:
        if rn <= 25:
            return 10
        if rn > 25 and rn <= 50:
            return 30
        if rn > 50:
            return 0
    if floor >= 5:
        if rn <= 30:
            return 0
        if rn > 30 and rn <= 60:
            return 30
        if rn > 60 and rn <= 90:
            return 20
        if rn > 90:
            return 10

def getmon(x, y):
    
    for i in range(len(enemies)):
        for j in range(len(enemies[i].diedin)):
            if enemies[i].diedin[j] == (room, floor, x, y):
                return ground

    #gets the monster that was already there
    for i in range(len(enemies)):
        if enemies[i].currentloc == ((room, floor), (x, y)) and enemies[i].loaded == False:
            if enemies[i].dead == False:
                enemies[i].loaded = True
                enemies[i].enx = x
                enemies[i].eny = y
                enemies[i].spawnx, enemies[i].spawny = x, y
                updatelog('view', enemies[i].name)
                return enemies[i].image

    #gets a random new monster
    temp = 0
    mon = getrandmon()
    monmax = mon + 9
    while True:
        if enemies[mon].dead == False and enemies[mon].currentloc == ((0, 0), (0, 0)):
            enemies[mon].enx = x
            enemies[mon].eny = y
            enemies[mon].spawnx, enemies[mon].spawny = x, y
            enemies[mon].loaded = True
            enemies[mon].rmfl = (room, floor)
            enemies[mon].currentloc = ((room, floor), (x, y))
            updatelog('view', enemies[mon].name)
            return enemies[mon].image
        else:
            mon += 1
        for i in range(len(enemies)):
            if enemies[i].dead == True:
                temp += 1
            if temp >= len(enemies) or mon > monmax:
                return ground

def placeboss(fl, x, y):
    if fl == 5:
        num = 0
    if fl == 10:
        num = 1
    if fl == 15:
        num = 2
    if bosses[num].hp > 1:
        bosses[num].enx = x
        bosses[num].eny = y
        bosses[num].loaded = True
        bosses[num].rmfl = (room, floor)
        bosses[num].currentloc = ((room, floor), (x, y))
        bosses[num].boss = True
        updatelog('view', bosses[num].name)
        return bosses[num].image
    else:
        return ground

def getitem(x, y, kind, bagkind = 0):

    swordlow = Item("Iron Sword", 'WEAP', 2, treasure, 6)
    swordmed = Item("Steel Sword", 'WEAP', 4, treasure, 8)
    swordhigh = Item("Platinum Sword", 'WEAP', 6, treasure, 10)
    daggerlow = Item("Iron Dagger", 'WEAP', 4, treasure, 4)
    daggermed = Item("Steel Dagger", 'WEAP', 6, treasure, 6)
    daggerhigh = Item("Platinum Dagger", 'WEAP', 8, treasure, 8)
    axelow = Item("Iron Axe", 'WEAP', 0, treasure, 8)
    axemed = Item("Steel Axe", 'WEAP', 2, treasure, 10)
    axehigh = Item("Platinum Axe", 'WEAP', 4, treasure, 12)

    swordsp = Item("Knight's Sword", 'WEAP', 8, treasure, 10)
    daggersp = Item("Goblin's Dagger", 'WEAP', 10, treasure, 8)
    axesp = Item("Axe of Guinea", 'WEAP', 4, treasure, 14)

    armorlow = Item("Iron Armor", 'ARM', 3, treasure)
    armormed = Item("Steel Armor", 'ARM', 6, treasure)
    armorhigh = Item("Platinum Armor", 'ARM', 9, treasure)

    weakpot = Item("Weak Potion", 'HEAL', 5, bag)
    pot = Item("Potion", 'HEAL', 10, bag)
    strpot = Item("Strong Potion", 'HEAL', 30, bag)
    ant = Item("Antidote", 'PSN', 0, bag)
    paraheal = Item("Paralysis Heal", 'PARA', 0, bag)
    speed = Item("Speed Potion", 'SPD', 0, bag)
    invpot = Item("Invincibility Potion", 'INV', 0, bag)

    if bagkind != 0: #for drops
        if bagkind == "Potion":
            tempitem = weakpot
        if bagkind == "Antidote":
            tempitem = ant
        tempitem.pos = (x, y)
        tempitem.rmfl = (room, floor)
        additem(items, tempitem)
        return tempitem.image

    for i in range(len(items)): #for items that were already there
        if items[i].rmfl == (room, floor) and items[i].pos == (x, y):
            if kind == 'T' and items[i].image == treasure and items[i].ininv == False:
                items[i].pos = (x, y)
                return items[i].image
            if kind == 'B' and items[i].image == bag and items[i].ininv == False:
                items[i].pos = (x, y)
                return items[i].image
            if items[i].ininv == True:
                return ground

    if kind == 'T':
        rn = random.randint(0, 100)
        if floor < 5:
            if rn <= 23:
                tempitem = swordlow
            if rn > 23 and rn <= 46:
                tempitem = daggerlow
            if rn > 46 and rn <= 69:
                tempitem = axelow
            if rn > 69 and rn <= 92:
                tempitem = armorlow
            if rn > 92:
                rn = random.randint(0, 100)
                if rn <= 25:
                    tempitem = swordmed
                if rn > 25 and rn <= 50:
                    tempitem = daggermed
                if rn > 50 and rn <= 75:
                    tempitem = axemed
                if rn > 75:
                    tempitem = armormed
        if floor >= 5 and floor < 10:
            if rn <= 23:
                tempitem = swordmed
            if rn > 23 and rn <= 46:
                tempitem = daggermed
            if rn > 46 and rn <= 69:
                tempitem = axemed
            if rn > 69 and rn <= 92:
                tempitem = armormed
            if rn > 92:
                rn = random.randint(0, 100)
                if rn <= 25:
                    tempitem = swordhigh
                if rn > 25 and rn <= 50:
                    tempitem = daggerhigh
                if rn > 50 and rn <= 75:
                    tempitem = axehigh
                if rn > 75:
                    tempitem = armorhigh
        if floor >= 10:
            if rn <= 60:
                rn = random.randint(0, 100)
                if rn <= 25:
                    tempitem = swordmed
                if rn > 25 and rn <= 50:
                    tempitem = daggermed
                if rn > 50 and rn <= 75:
                    tempitem = axemed
                if rn > 75:
                    tempitem = armormed
            if rn > 60:
                rn = random.randint(0, 100)
                if rn <= 25:
                    tempitem = swordhigh
                if rn > 25 and rn <= 50:
                    tempitem = daggerhigh
                if rn > 50 and rn <= 75:
                    tempitem = axehigh
                if rn > 75:
                    tempitem = armorhigh

    if kind == 'B':
        rn = random.randint(0, 100) #get new item
        if floor < 5:
            if rn <= 70:
                tempitem = weakpot
            if rn > 70:
                tempitem = ant
        if floor >= 5 and floor < 10:
            if rn <= 30:
                tempitem = pot
            if rn > 30 and rn <= 40:
                tempitem = speed
            if rn > 40 and rn <= 60:
                tempitem = weakpot
            if rn > 60 and rn <= 80:
                tempitem = ant
            if rn > 80:
                tempitem = paraheal
        if floor >= 10:
            if rn <= 5:
                tempitem = invpot
            if rn > 5 and rn <= 15:
                tempitem = speed
            if rn > 15 and rn <= 30:
                tempitem = ant
            if rn > 30 and rn <= 50:
                tempitem = paraheal
            if rn > 50 and rn <= 70:
                tempitem = strpot
            if rn > 70:
                tempitem = pot
    tempitem.pos = (x, y)
    tempitem.rmfl = (room, floor)
    additem(items, tempitem)
    return tempitem.image

def pickup():
    global keypos, haskey, invmax, itemrmflxy
    if (plx, ply) == keypos:
        haskey = True
        keyused.append((room, floor))
        foremap[plx][ply] = player 
        backmap[plx][ply] = ground
        updatelog('pick', "key")
    for i in range(len(items)):
        if items[i].pos == (plx, ply) and items[i].rmfl == (room, floor):
            items[i].ininv = True
            if items[i].dropped == False:
                rmflxy = (items[i].rmfl, items[i].pos)
                itemrmflxy.append(rmflxy)
            items[i].pos = (0, 0)
            backmap[plx][ply] = ground
            invmax += 1
            updatelog('pick', items[i].name)

def openinv():
    cursor = 0
    while True:
        screen.fill(pygame.Color("black"), (0, 0, 500, 500))
        temp = 0
        done = False
        for i in range(len(items)):
            if items[i].ininv == True:
                screen.blit(log.render(items[i].name + "    " + str(items[i].value), True, pygame.Color("white")), (50, (temp * 50) + 50))
                items[i].curs = temp
                temp += 1
            if items[i].equip == True:
                screen.blit(log.render("*", True, pygame.Color("white")), (40, (items[i].curs * 50) + 50))
            if items[i].equip == False:
                screen.fill(pygame.Color("black"), (38, (items[i].curs * 50) + 48, 15, 10))
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
                i = 0
                trueornot = False
                while not done:
                    if items[i].curs == cursor:
                        if cursor - 1 != -1 and items[i].kind != "WEAP" and items[i].kind != "ARM":
                            cursor -= 1
                        trueornot = items[i].use()
                        j = i
                        for j in range(i, len(items)):
                            if trueornot == True:
                                items[j].listpos -= 1
                        done = True
                    i += 1
                    if i >= len(items):
                        done = True
            if select.key == pygame.K_d:
                for i in range(len(items)):
                    if items[i].curs == cursor:
                        items[i].drop()
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
def loadmap(direct):
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
        for i in range(len(enemies)):
            enemies[i].recycle(True)
    if direct == 'STAIR_DOWN':
        downstrpos = (0, 0)
        floor += 1
        for i in range(len(enemies)):
            enemies[i].recycle(True)

    if (floor, room) == (5, 2) and direct == 'RIGHT':
        ply = 1
    """if (floor, room) == (10, x):
        pl = num
    if (floor, room) == (15, x):
        pl = num"""

    newmap = "rooms/fl" + str(floor) + "r" + str(room) + ".txt"
    newmap = open(newmap, 'r')
    newmap = newmap.read()
    newmap = newmap.replace('\n' , '')

    for i in range(10):
        for j in range(10):
            backmap[i][j] = newmap[i * 10 + j]

    for i in range(10):
        for j in range(10):

            for k in range(len(items)): #for items that were dropped
                if (i, j) == items[k].pos and (room, floor) == items[k].rmfl:
                    foremap[i][j] = bag
                    backmap[i][j] = foremap[i][j]

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
            if backmap[i][j] == 'Q':
                foremap[i][j] = placeboss(floor, i, j)
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
                tracker = 0
                for k in range(len(itemrmflxy)):
                    if ((room, floor), (i, j)) == itemrmflxy[k]:
                        tracker += 1
                if tracker == 0:
                    foremap[i][j] = getitem(i, j, 'B')
                else:
                    foremap[i][j] = ground
                backmap[i][j] = foremap[i][j]
            if backmap[i][j] == '<':
                foremap[i][j] = upstair
                backmap[i][j] = upstair
                upstrpos = (i, j)
            if backmap[i][j] == '>':
                foremap[i][j] = downstair
                backmap[i][j] = downstair
                downstrpos = (i, j)

#it's terrible, I know
def move(x):
    global foremap, plx, ply, haskey, dooropen, paracount

    if para == True:
        paracount += 1
        return

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
        for i in range(len(bosses)):
            if plx - 1 == bosses[i].enx and ply == bosses[i].eny and foremap[plx - 1][ply] == bosses[i].image and load == False:
                bosses[i].hp = attack(bosses[i], weapon)
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
        for i in range(len(bosses)):
           if plx + 1 == bosses[i].enx and ply == bosses[i].eny and foremap[plx + 1][ply] == bosses[i].image and load == False:
                bosses[i].hp = attack(bosses[i], weapon)
                attacked = True

        if foremap[plx + 1][ply] != wall and foremap[plx + 1][ply] != statue and foremap[plx + 1][ply] != door and load == False and attacked == False:
            plx += 1

    if x == 'LEFT':
        if ply == 0:
            loadmap('LEFT')
            load = True

        for i in range(len(enemies)):
           if plx == enemies[i].enx and ply - 1 == enemies[i].eny and foremap[plx][ply - 1] == enemies[i].image and load == False:
                enemies[i].hp = attack(enemies[i], weapon)
                attacked = True
        for i in range(len(bosses)):
           if plx == bosses[i].enx and ply - 1 == bosses[i].eny and foremap[plx][ply - 1] == bosses[i].image and load == False:
                bosses[i].hp = attack(bosses[i], weapon)
                attacked = True

        if foremap[plx][ply - 1] != wall and foremap[plx][ply - 1] != statue and foremap[plx][ply - 1] != door and load == False and attacked == False:
            ply -= 1

    if x == 'RIGHT':
        if ply == 9:
            loadmap('RIGHT')
            load = True

        for i in range(len(enemies)):
          if plx == enemies[i].enx and ply + 1 == enemies[i].eny and foremap[plx][ply + 1] == enemies[i].image and load == False:
                enemies[i].hp = attack(enemies[i], weapon)
                attacked = True
        for i in range(len(bosses)):
          if plx == bosses[i].enx and ply + 1 == bosses[i].eny and foremap[plx][ply + 1] == bosses[i].image and load == False:
                bosses[i].hp = attack(bosses[i], weapon)
                attacked = True

        if foremap[plx][ply + 1] != wall and foremap[plx][ply + 1] != statue and foremap[plx][ply + 1] != door and load == False and attacked == False:
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
            floor = 5
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

    if speedcount == 3:
        speed == False
        speedcount = 0
        speedturn = 0

    if speed == False or speedturn == 1:
        for i in range(len(enemies)):
            enemies[i].die()
            if enemies[i].dead == False:
                tempgo = enemies[i].keepgo
                enemies[i].keepgo = enemies[i].enmv(tempgo)
            else:
                if enemies[i].drop != None and enemies[i].drop != 0:
                    foremap[enemies[i].enx][enemies[i].eny] = enemies[i].drop
                    backmap[enemies[i].enx][enemies[i].eny] = enemies[i].drop
                screen.blit(foremap[enemies[i].enx][enemies[i].eny], (enemies[i].enx * 50, enemies[i].eny * 50))
                pygame.display.update()
                enemies[i].enx, enemies[i].eny = 0, 0
                enemies[i].recycle()
        for i in range(1):
            bosses[i].die()
            if bosses[i].dead == False:
                tempgo = bosses[i].keepgo
                bosses[i].keepgo = bosses[i].enmv(tempgo)
            else:
                if bosses[i].drop != None and bosses[i].drop != 0:
                    foremap[bosses[i].enx][bosses[i].eny] = bosses[i].drop
                    backmap[bosses[i].enx][bosses[i].eny] = bosses[i].drop
                screen.blit(foremap[bosses[i].enx][bosses[i].eny], (bosses[i].enx * 50, bosses[i].eny * 50))
                pygame.display.update()
                bosses[i].enx, bosses[i].eny = 0, 0
        speedcount += 1
        speedturn = 0
    elif speed == True:
        speedturn += 1

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

    if psn == True:
        screen.blit(log.render("PSN", True, pygame.Color("purple")), (300, 500))
        if psnstep % 4 == 0:
            plhp -= 1
        if psnstep >= 100:
            psn = False
        psnstep += 1
    if para == True:
        screen.blit(log.render("PARA", True, pygame.Color("red")), (350, 500))
        paracount += 1
        if paracount == paramax:
            para = False
            paracount = 0
    if nodam == True:
        screen.blit(log.render("INV", True, pygame.Color("yellow")), (350, 520))
        nodamcount += 1
        if nodamcount == 5:
            screen.fill(pygame.Color("black"), (349, 520, 40, 15))
            nodam = False
            nodamcount = 0
    if speed == True:
        screen.blit(log.render("SPD", True, pygame.Color("cyan")), (300, 520))
    if speed == False:
        screen.fill(pygame.Color("black"), (299, 520, 40, 15))
    if psn == False:
        screen.fill(pygame.Color("black"), (299, 500, 40, 15))
    if para == False:
        screen.fill(pygame.Color("black"), (349, 500, 40, 15))

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
    level = levelup(nextlvl[level])
    pygame.display.update()
