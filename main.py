import pygame
import sys
import random
import pdb

pygame.init()

screen = pygame.display.set_mode((500, 600))
pygame.display.set_caption("A Hot Tennessee Knight")
pygame.event.set_allowed(None)
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN])
pygame.font.init()

log = pygame.font.SysFont("monospace", 14)
med = pygame.font.SysFont("monospace", 28)
big = pygame.font.SysFont("monospace", 50)
text = [log.render("", True, pygame.Color("black")) for i in range(5)] #for the updatelog function

debug = False

#Title Screen
title1 = big.render("A Hot", True, pygame.Color("green"))
title2 = big.render("Tennessee", True, pygame.Color("green"))
title3 = big.render("Knight", True, pygame.Color("green"))
options = [
log.render("Start Game", True, pygame.Color("white")),
log.render("Debug", True, pygame.Color("white"))
]
screen.blit(title1, (50, 75))
screen.blit(title2, (100, 125))
screen.blit(title3, (225, 175))
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
guinea = pygame.image.load('graphics/guinea.png').convert()
megabat = pygame.image.load('graphics/megabat.png').convert()
mammoth = pygame.image.load('graphics/mammoth.png').convert()
monster = pygame.image.load('graphics/monster.png').convert()
knight = pygame.image.load('graphics/knight.png').convert()
ghost = pygame.image.load('graphics/ghost.png').convert()
littleeagle = pygame.image.load('graphics/littleeagle.png').convert()
troll = pygame.image.load('graphics/troll.png').convert()
troll2 = pygame.image.load('graphics/troll2.png').convert()
skeleton = pygame.image.load('graphics/skeleton.png').convert()
skeleton2 = pygame.image.load('graphics/skeleton2.png').convert()
kingpig = pygame.image.load('graphics/kingpig.png').convert()
bigeagle = pygame.image.load('graphics/bigeagle.png').convert()
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
flash = False
flashcount = 0
flashmax = 0
armoron = False
nextlvl = [0 for i in range(50)]
nextlvl[1] = 10
for i in range(2, 50):
    nextlvl[i] = nextlvl[i - 1] * 1.25 + 1
    nextlvl[i] = int(nextlvl[i])
platt = 1
armor = 10
invmax = -1
invmaxmax = 17
itemrmflxy = [((0, 0), (0, 0))]
haskey = [0, 0, 0, 0]

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
screen.blit(log.render("HP: " + str(plhp) + "/" + str(maxhp), True, pygame.Color("white")), (0, 500))
screen.blit(log.render("XP: " + str(xp) + "/" + str(nextlvl[level]), True, pygame.Color("white")), (80, 500))
screen.blit(log.render("Att: " + str(platt), True, pygame.Color("white")), (190, 500))
screen.blit(log.render("Def: " + str(armor), True, pygame.Color("white")), (260, 500))

pygame.mixer.init()
bgm = pygame.mixer.Sound('music/BGM1.ogg')
bgm.play(-1)

skelgo = 'UP'
multiroomboss = False
loadedroom = False
telecount = 0
finalset = False
littlespawn = True
bossstart = False

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

def updatelog(kind, thing = 0, value = 0):  #55 characters is the max string length
    global text
    text[4] = text[3]
    text[3] = text[2]
    text[2] = text[1]
    text[1] = text[0]
    newlog = pygame.Rect(0, 585, 600, 15)
    thing = str(thing)
    value = str(value)

    screen.fill(pygame.Color("black"), (0, 515, 450, 85))
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
    if kind == 'enmiss':
        text[0] = log.render("The " + thing + " misses you", True, pygame.Color("white"))
    if kind == 'crit':
        if thing == "Goblin":
            text[0] = log.render("The Goblin wraps its tie around you!", True, pygame.Color("red"))
        if thing == "Rat":
            text[0] = log.render("The Rat goes for your ankles!", True, pygame.Color("red"))
        if thing == "Snake":
            text[0] = log.render("The Snake sidles up and coils!", True, pygame.Color("red"))
        if thing == "Guinea Pig":
            text[0] = log.render("The Guinea Pig gives you a karate kick!", True, pygame.Color("red"))
        if thing == "Megabat":
            text[0] = log.render("The Bat buffets you mightily with its wings!", True, pygame.Color("red"))
        if thing == "Mammoth":
            text[0] = log.render("The Mammoth stomps you!", True, pygame.Color("red"))
        if thing == "Monster":
            text[0] = log.render("The Monster gets you around the throat!", True, pygame.Color("red"))
        if thing == "Troll":
            text[0] = log.render("The Troll smashes you with its turkey leg!", True, pygame.Color("red"))
        if thing == "Knight":
            text[0] = log.render("The Knight tries a leaping attack!", True, pygame.Color("red"))
        if thing == "Ghost":
            text[0] = log.render("The Ghost kicks you in the shins!", True, pygame.Color("red"))
        if thing == "Skeleton":
            text[0] = log.render("The Skeleton slashes wildly with the knife!", True, pygame.Color("red"))
        if thing == "Little-Eagle":
            text[0] = log.render("The Little-Eagle goes for your eyes!", True, pygame.Color("red"))
    if kind == 'nodam':
        text[0] = log.render("The " + thing + " hits you but you don't take any damage", True, pygame.Color("white"))
    if kind == 'magi':
        text[0] = log.render("The " + thing + " shoots a fireball at you", True, pygame.Color("red"))
    if kind == 'magihit':
        text[0] = log.render("It hits for " + value + " damage", True, pygame.Color("red"))
    if kind == 'magimiss':
        text[0] = log.render("It misses", True, pygame.Color("white"))
    if kind == "telein":
        text[0] = log.render("The " + thing + " appears out of thin air", True, pygame.Color("white"))
    if kind == "teleout":
        text[0] = log.render("The " + thing + " vanishes before your eyes", True, pygame.Color("white"))
    if kind == 'sur':
        text[0] = log.render("You are surrounded!", True, pygame.Color("white"))
    if kind == 'pick':
        text[0] = log.render("You pick up the " + thing, True, pygame.Color("white"))
    if kind == 'drop':
        text[0] = log.render("You dropped the " + thing, True, pygame.Color("white"))
    if kind == 'invmax':
        text[0] = log.render("You inventory is full", True, pygame.Color("white"))
    if kind == 'eqarmor':
        text[0] = log.render("You put on the " + thing, True, pygame.Color("white"))
    if kind == 'unarmor':
        text[0] = log.render("You take off the " + thing, True, pygame.Color("white"))
    if kind == 'eqweap':
        text[0] = log.render("You wield the " + thing, True, pygame.Color("white"))
    if kind == 'unweap':
        text[0] = log.render("You put away the " + thing, True, pygame.Color("white"))
    if kind == 'wrongkey':
        text[0] = log.render("The key doesn't seem to fit", True, pygame.Color("white"))
    if kind == 'nokey':
        text[0] = log.render("You need a key to open this", True, pygame.Color("white"))
    if kind == 'bossdoor':
        text[0] = log.render("All the doors close", True, pygame.Color("white"))
    if kind == 'heal':
        text[0] = log.render("You healed yourself for " + thing + " damage", True, pygame.Color("yellow"))
    if kind == 'ant':
        text[0] = log.render("You recovered from the poison", True, pygame.Color("purple"))
    if kind == 'paraheal':
        text[0] = log.render("You recovered from the paralysis", True, pygame.Color("red"))
    if kind == 'psnheal':
        text[0] = log.render("The poison died down", True, pygame.Color("purple"))
    if kind == 'paraheal2':
        text[0] = log.render("The paralysis wore off", True, pygame.Color("red"))
    if kind == 'psn':
        text[0] = log.render("The poison damages you", True, pygame.Color("purple"))
    if kind == 'psninit':
        text[0] = log.render("You have been poisoned!", True, pygame.Color("purple"))
    if kind == 'para':
        text[0] = log.render("You can't move", True, pygame.Color("red"))
    if kind == 'parainit':
        text[0] = log.render("You got paralyzed!", True, pygame.Color("red"))
    if kind == 'flash':
        text[0] = log.render("The room lights up in a blinding flash!", True, pygame.Color("white"))
    if kind == 'flash2':
        text[0] = log.render("The Enemies are stunned and cannot move!", True, pygame.Color("white"))
    if kind == 'level':
        text[0] = log.render("You are now level " + thing, True, pygame.Color("green"))
    if kind == 'stat':
        text[0] = log.render("Your " + thing + " stat went up by " + value, True, pygame.Color("green"))
    if kind == 'dead':
        text[0] = log.render("You died", True, pygame.Color("red"))
    if kind == 'win':
        text[0] = log.render("Congratulations! You beat the game!", True, pygame.Color("green"))
    if kind == 'kill':
        if value == 'sword':
            if thing == "Goblin":
                text[0] = log.render("You slash the Goblin's head off", True, pygame.Color("blue"))
            if thing == "Rat":
                text[0] = log.render("You slice off the Rat's tail", True, pygame.Color("blue"))
            if thing == "Snake":
                text[0] = log.render("You slice the Snake into bits", True, pygame.Color("blue"))
            if thing == "Guinea Pig":
                text[0] = log.render("You cut off it's back-left leg", True, pygame.Color("blue"))
            if thing == "Megabat":
                text[0] = log.render("You cut off the Bat's wings", True, pygame.Color("blue"))
            if thing == "Mammoth":
                text[0] = log.render("You slice off it's trunk", True, pygame.Color("blue"))
            if thing == "Monster":
                text[0] = log.render("You impale it's smug face", True, pygame.Color("blue"))
            if thing == "Troll":
                text[0] = log.render("You cut off the Troll's club arm", True, pygame.Color("blue"))
            if thing == "Knight":
                text[0] = log.render("You slash at the gaps of it's armor", True, pygame.Color("blue"))
            if thing == "Ghost":
                text[0] = log.render("You slice up the ectoplasma", True, pygame.Color("blue"))
            if thing == "Skeleton":
                text[0] = log.render("You sever the bone connections", True, pygame.Color("blue"))
            if thing == "Little-Eagle":
                text[0] = log.render("You slice the feathers off it's head", True, pygame.Color("blue"))
        if value == 'dagger':
            if thing == "Goblin":
                text[0] = log.render("You shank the Goblin", True, pygame.Color("blue"))
            if thing == "Rat":
                text[0] = log.render("You turn the Rat into a raw shish kabob", True, pygame.Color("blue"))
            if thing == "Snake":
                text[0] = log.render("You skin the Snake alive", True, pygame.Color("blue"))
            if thing == "Guinea Pig":
                text[0] = log.render("You disembowel the Guinea Pig", True, pygame.Color("blue"))
            if thing == "Megabat":
                text[0] = log.render("You jam the knife into its vital organs", True, pygame.Color("blue"))
            if thing == "Mammoth":
                text[0] = log.render("You cut its legs off", True, pygame.Color("blue"))
            if thing == "Monster":
                text[0] = log.render("You cut off its stupid gloves", True, pygame.Color("blue"))
            if thing == "Troll":
                text[0] = log.render("You poke out its eye", True, pygame.Color("blue"))
            if thing == "Knight":
                text[0] = log.render("You slit its throat", True, pygame.Color("blue"))
            if thing == "Ghost":
                text[0] = log.render("You cut its sheet up", True, pygame.Color("blue"))
            if thing == "Skeleton":
                text[0] = log.render("You cut off its chain", True, pygame.Color("blue"))
            if thing == "Little-Eagle":
                text[0] = log.render("You stab the bird in the foot", True, pygame.Color("blue"))
        if value == 'axe':
            if thing == "Goblin":
                text[0] = log.render("You split it down the middle", True, pygame.Color("blue"))
            if thing == "Rat":
                text[0] = log.render("You give it a nice axe hair-cut", True, pygame.Color("blue"))
            if thing == "Snake":
                text[0] = log.render("You chop it up like you would a carrot", True, pygame.Color("blue"))
            if thing == "Guinea Pig":
                text[0] = log.render("You cut off its 14 toes", True, pygame.Color("blue"))
            if thing == "Megabat":
                text[0] = log.render("You brake the Bat", True, pygame.Color("blue"))
            if thing == "Mammoth":
                text[0] = log.render("You cut it open, but don't drink its blood", True, pygame.Color("blue"))
            if thing == "Monster":
                text[0] = log.render("You chop the Monster into 8 pieces", True, pygame.Color("blue"))
            if thing == "Troll":
                text[0] = log.render("You chop the Troll into 4 pieces", True, pygame.Color("blue"))
            if thing == "Knight":
                text[0] = log.render("You bash its skull into two", True, pygame.Color("blue"))
            if thing == "Ghost":
                text[0] = log.render("You banish the Ghost", True, pygame.Color("blue"))
            if thing == "Skeleton":
                text[0] = log.render("You knock the Skeleton's remaining teeth out", True, pygame.Color("blue"))
            if thing == "Little-Eagle":
                text[0] = log.render("You cut it open and drink its blood", True, pygame.Color("blue"))
    
    screen.blit(text[0], newlog)

def levelup(lvlxp):
    global xp, maxhp, platt, armor, plhp
    if xp >= lvlxp:
        rnstat = 0
        cursor = 0
        updatelog('level', level + 1)
        stats = ["HP", "Attack", "Defence"]

        rn = random.randint(2, 4)
        maxhp += rn
        updatelog('stat', "HP", rn)
        rn = random.randint(1, 2)
        platt += rn
        updatelog('stat', "attack", rn)
        rn = random.randint(1, 2)
        armor += rn
        updatelog('stat', "defence", rn)

        screen.fill(pygame.Color("black"), (0, 515, 600, 85))
        for i in range(len(stats)):
            screen.blit(log.render(stats[i], True, pygame.Color("white")), (30, 525 + i * 20))
        screen.blit(log.render("__", True, pygame.Color("white")), (30, 528))
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
            if cursor == 0:
                cursline = "_" * len("HP")
            if cursor == 1:
                cursline = "_" * len("Attack")
            if cursor == 2:
                cursline = "_" * len("Defence")
            screen.blit(log.render(cursline, True, pygame.Color("white")), (30, (cursor * 20) + 528))
            pygame.display.update()


        if choice == "HP":
            rnstat = random.randint(1, 2)
            updatelog('stat', "HP", rnstat)
            maxhp += rnstat    
        if choice == "Attack":
            updatelog('stat', "attack", 1)
            platt += 1
        if choice == "Defence":
            updatelog('stat', "defence", 1)
            armor += 1

        screen.fill(pygame.Color("black"), (25, 500, 23, 15))
        screen.fill(pygame.Color("black"), (55, 500, 23, 15))
        screen.blit(log.render(str(plhp), True, pygame.Color("white")), (32, 500))
        screen.blit(log.render(str(maxhp), True, pygame.Color("white")), (55, 500))
        plhp = maxhp
        xp = xp - lvlxp
        return level + 1
    else:
        return level 

class Item():
    pos = (0, 0)
    rmfl = (0, 0)
    row = None
    col = None
    listpos = None
    equip = False
    ininv = False
    dropped = False
    def __init__(self, name, kind, value, image, damage = 0, weaptype = 0): #damage is for weapons
        self.name = name
        self.kind = kind
        self.value = value
        self.image = image
        self.damage = damage
        self.weaptype = weaptype

    def drop(self):
        global invmax, foremap, items, backmap
        if self.ininv == True:
            self.ininv = False
            self.dropped = True
            self.equip = False
            invmax -= 1
            self.pos = (plx, ply)
            self.rmfl = (room, floor)
            updatelog('drop', self.name)
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
        global weapon, plhp, maxhp, armor, armoron, psn, para
        if self.kind == 'WEAP':
            screen.fill(pygame.Color("black"), (229, 500, 20, 15))
            if self.equip == False and weapon == "fist":
                self.equip = True
                weapon = self
                screen.blit(log.render(str(platt + weapon.value), True, pygame.Color("white")), (230, 500))
                updatelog('eqweap', self.name)
            elif self.equip == True:
                self.equip = False
                weapon = "fist"
                screen.blit(log.render(str(platt), True, pygame.Color("white")), (230, 500))
                updatelog('unweap', self.name)
        if self.kind == 'ARM':
            if self.equip == False and armoron == False:
                self.equip = True
                armoron = True
                armor += self.value
                updatelog('eqarmor', self.name)
            elif self.equip == True:
                self.equip = False
                armoron = False
                armor -= self.value
                updatelog('unarmor', self.name)
            screen.fill(pygame.Color("black"), (299, 500, 20, 15))
            screen.blit(log.render(str(armor), True, pygame.Color("white")), (300, 500))
        if self.kind == 'HEAL' and self.ininv == True:
            if self.value + plhp > maxhp:
                updatelog('heal', maxhp - plhp)
                plhp = maxhp
            else:
                plhp += self.value
                updatelog('heal', self.value)
            self.useitem()
            screen.fill(pygame.Color("black"), (25, 500, 23, 15))
            screen.blit(log.render(str(plhp), True, pygame.Color("white")), (32, 500))
            return True
        if self.kind == 'PSN' and self.ininv == True:
            if psn == True:
                psn = False
                self.useitem()
                screen.fill(pygame.Color("black"), (324, 500, 30, 15))
                updatelog('ant')
                return True
        if self.kind == 'PARA' and self.ininv == True:
            if para == True:
                para = False
                self.useitem()
                screen.fill(pygame.Color("black"), (354, 500, 45, 15))
                updatelog('paraheal')
                return True
        if self.kind == 'ALL' and self.ininv == True:
            if para == True or psn == True:
                para = False
                psn = False
                self.useitem()
                return True
        if self.kind == 'SPD' and self.ininv == True:
            global speed
            if speed == False:
                speed = True
                self.useitem()
                screen.blit(log.render("SPD", True, pygame.Color("cyan")), (390, 500))
                return True
        if self.kind == 'INV' and self.ininv == True:
            global nodam
            if nodam == False:
                nodam = True
                self.useitem()
                screen.blit(log.render("INV", True, pygame.Color("yellow")), (420, 500))
                return True
        if self.kind == 'FLSH' and self.ininv == True:
            global flash, flashcount
            flash = True
            flashcount = 0
            self.useitem()
            updatelog('flash')
            updatelog('flash2')
            return True

items = [Item("Potion", 'HEAL', 5, bag)]

def additem(itemlist, itemobj):
    itemobj.listpos = len(itemlist)
    return itemlist.append(itemobj)

def restorelistpos(itemlist):
    for i in range(len(itemlist)):
        itemlist[i].listpos = i
    return itemlist

def iteminv(itemlist):
    newitemlist = []
    for i in range(len(itemlist)):
        if itemlist[i].ininv == True:
            newitemlist.append(itemlist[i])
    if newitemlist != []:
        return newitemlist

#the enemy class    This is magic code now. I have forgotten what most of this is and how it works. I just know it works badly.
class Enemy():
    enx, eny = 0, 0
    spawnx, spawny = 0, 0
    drop = 0
    loaded = False
    dead = False
    boss = False
    teleported = False
    xpused = False
    ghostinv = False
    invcount = 0
    keepgo = 'UP'
    stage = 0
    enroom = 0
    rmfl = (0, 0)
    currentloc = ((0, 0), (0, 0)) # room, floor, x, y
    diedin = [(0, 0, 0, 0)] # same as ^ but worse and I don't want to change it
    def __init__(self, name, hp, att, armor, damage, xp, image):
        self.name = name
        self.hp = hp
        self.temphp = hp
        self.att = att
        self.armor = armor
        self.damage = damage
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

    def enatt(self, hp, spec = 0):
        global psn, para, paramax, armor
        if self.loaded == True and nodam == False:

            dam = 0
            rn = random.randint(1, 20)
            if rn + self.att >= armor:
                dam = random.randint(1, self.damage)
            elif rn == 20:
                dam = self.damage * 2
                updatelog('crit', self.name)

            if dam != 0:
                updatelog('dam', self.name, dam)
            elif dam == 0:
                updatelog('enmiss', self.name)

            if dam != 0:
                rnstatus = random.randint(1, 100)
                if spec == "para":
                    para = True
                    paramax = random.randint(1, 10)
                    updatelog('parainit')
                if self.name == "Rat":
                    if rnstatus <= 10:
                        psn = True
                        updatelog('psninit')
                if self.name == "Snake":
                    if rnstatus <= 5:
                        psn = True
                        updatelog('psninit')
                    if rnstatus > 5 and rnstatus <= 10:
                        para = True
                        paramax = 10
                        updatelog('parainit')
                if self.name == "Megabat":
                    if rnstatus <= 20:
                        psn = True
                        updatelog('psninit')
                if self.name == "Monster":
                    if rnstatus <= 20:
                        para = True
                        paramax = 12
                        updatelog('parainit')
                if self.name == "Skeleton":
                    if rnstatus <= 20:
                        para = True
                        paramax = 8
                        updatelog('parainit')
                if self.name == "Big-Eagle" and self.stage == 3:
                    if random.randint(1, 100) <= 10:
                        self.tele()
            return hp - dam
        elif self.loaded == True and nodam == True:
            updatelog('nodam', self.name)
            return hp

    def enmv(self, direct): #at least it works
        global foremap, plhp, flash, flashcount, flashmax

        if flashcount >= flashmax:
            flash = False
            flashcount = 0
            flashmax = 0
        if flash == True and self.loaded == True:
            flashcount += 1
            return 'UP'

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
        if self.loaded == True and attacked == False and self.hp > 0:

            foremap[self.enx][self.eny] = backmap[self.enx][self.eny]

            if self.los() == True:
                if self.enx < plx and down == ground or down == bag or down == treasure or down == upstair or down == downstair or down == key:
                    self.enx += 1
                elif self.enx > plx and up == ground or up == bag or up == treasure or up == upstair or up == downstair or up == key:
                    self.enx -= 1
                elif self.eny < ply and right == ground or right == bag or right == treasure or right == upstair or right == downstair or right == key:
                    self.eny += 1
                elif self.eny > ply and left == ground or left == bag or left == treasure or left == upstair or left == downstair or left == key:
                    self.eny -= 1

            else:
                if direct == 'DOWN':
                    if down == ground or down == bag or down == treasure or down == upstair or down == downstair or down == key:
                        self.enx += 1
                    else:
                        foremap[self.enx][self.eny] = self.image
                        return leri
                elif direct == 'UP':
                    if up == ground or up == bag or up == treasure or up == upstair or up == downstair or up == key:
                        self.enx -= 1
                    else:
                        foremap[self.enx][self.eny] = self.image
                        return leri
                elif direct == 'RIGHT':
                    if right == ground or right == bag or right == treasure or right == upstair or right == downstair or right == key:
                        self.eny += 1
                    else:
                        foremap[self.enx][self.eny] = self.image
                        return updo
                elif direct == 'LEFT':
                    if left == ground or left == bag or left == treasure or left == upstair or left == downstair or left == key:
                        self.eny -= 1
                    else:
                        foremap[self.enx][self.eny] = self.image
                        return updo

            foremap[self.enx][self.eny] = self.image
        return direct

    def tele(self):
        foremap[self.enx][self.eny] = backmap[self.enx][self.eny]
        updatelog("teleout", self.name)
        self.enx, self.eny = 5, 5
        self.teleported = True
        rn = random.randint(0, 2)
        if rn == 0:
            if self.enroom != 1 or self.enroom != 4:
                self.enroom -= 1
            else:
                self.enroom += 1
        if rn == 1:
            if self.enroom != 3 or self.enroom != 6:
                self.enroom += 1
            else:
                self.enroom -= 1
        if rn == 2:
            if self.enroom >= 4:
                self.enroom -= 3
            else:
                self.enroom += 3

    def skellycheck(self, xy):
        #for the x axis
        if xy == True:
            x1 = self.enx
            x2 = self.enx
            #is there a better way to do this?
            while foremap[x1][self.eny] != wall and foremap[x1][self.eny] != statue and foremap[x1][self.eny] != door and x1 + 1 < 10:
                x1 += 1
            while foremap[x2][self.eny] != wall and foremap[x2][self.eny] != statue and foremap[x2][self.eny] != door and x2 - 1 > -1:
                x2 -= 1
            if x1 - self.enx > self.enx - x2 and foremap[self.enx + 1][self.eny] == ground:
                self.enx += 1
                return 'DOWN'
            elif foremap[self.enx - 1][self.eny] == ground:
                self.enx -= 1
                return 'UP'
        #for the y axis
        if xy == False:
            y1 = self.eny
            y2 = self.eny
            while foremap[self.enx][y1] != wall and foremap[self.enx][y1] != statue and foremap[self.enx][y1] != door and y1 + 1 < 10:
                y1 += 1
            while foremap[self.enx][y1] != wall and foremap[self.enx][y1] != statue and foremap[self.enx][y1] != door and y2 - 1 > -1:
                y2 -= 1
            if y1 - self.eny > self.eny - y2 and foremap[self.enx][self.eny + 1] == ground:
                self.eny += 1
                return 'RIGHT'
            elif foremap[self.enx][self.eny - 1] == ground:
                self.eny -= 1
                return 'LEFT'

    def forskellymagic(self, hp):
        #animations?
        rn = random.randint(1, 10)
        updatelog('magi', self.name)
        if rn <= 5:
            rndam = random.randint(10, 20)
            updatelog('magihit', None, rndam)
            return hp - rndam
        else:
            updatelog('magimiss')
            return hp

    #what is a subclass?
    def forskellyonly(self, keepgoskel):
        global foremap, plhp
        moved = False
        direct = keepgoskel
        enpos = (self.enx, self.eny)
        rn = random.randint(0, 10)
        if (self.enx - 1 == plx or self.enx + 1 == plx) and self.eny == ply:
            if self.name == "Big-Eagle" and self.stage == 2:
                rn = random.randint(1, 10)
                if rn <= 3:
                    self.tele()
                    return 'UP'
            if rn <= 3:
                if self.enx + 1 <= 9 and self.enx - 1 == plx and foremap[self.enx + 1][self.eny] == ground:
                    if self.name == "Big-Eagle":
                        plhp = self.enatt(plhp, "para")
                    foremap[self.enx][self.eny] = backmap[self.enx][self.eny]
                    self.enx += 1
                    direct = 'DOWN'
                elif self.enx - 1 >= 0 and self.enx + 1 == plx and foremap[self.enx - 1][self.eny] == ground:
                    if self.name == "Big-Eagle":
                        plhp = self.enatt(plhp, "para")
                    foremap[self.enx][self.eny] = backmap[self.enx][self.eny]
                    self.enx -= 1
                    direct = 'UP'
                else:
                    if self.name == "Big-Eagle":
                        plhp = self.enatt(plhp, "para")
                    foremap[self.enx][self.eny] = backmap[self.enx][self.eny]
                    direct = self.skellycheck(False)
                foremap[self.enx][self.eny] = self.image
                moved = True
                if rn > 3 or enpos == (self.enx, self.eny):
                    plhp = self.enatt(plhp)
                    moved = False
                return direct
        if self.enx == plx and (self.eny + 1 == ply or self.eny - 1 == ply):
            if self.name == "Big-Eagle" and self.stage == 2:
                rn = random.randint(1, 10)
                if rn <= 3:
                    self.tele()
                    return 'UP'
            if rn <= 3:
                if self.eny + 1 <= 9 and self.eny - 1 == ply and foremap[self.enx][self.eny + 1] == ground:
                    if self.name == "Big-Eagle":
                        plhp = self.enatt(plhp, "para")
                    foremap[self.enx][self.eny] = backmap[self.enx][self.eny]
                    self.eny += 1
                    direct = 'RIGHT'
                elif self.eny - 1 >= 0 and self.eny + 1 == ply and foremap[self.enx][self.eny - 1] == ground:
                    if self.name == "Big-Eagle":
                        plhp = self.enatt(plhp, "para")
                    foremap[self.enx][self.eny] = backmap[self.enx][self.eny]
                    self.eny -= 1
                    direct = 'LEFT'
                else:
                    if self.name == "Big-Eagle":
                        plhp = self.enatt(plhp, "para")
                    foremap[self.enx][self.eny] = backmap[self.enx][self.eny]
                    direct = self.skellycheck(True)
                foremap[self.enx][self.eny] = self.image
                moved = True
            if rn > 3 or enpos == (self.enx, self.eny):
                plhp = self.enatt(plhp)
                moved = False
            return direct
        else:
            #checks each direction to see if they are more than 2 spaces away from the player
            if moved == False and self.enx - plx >= 2 or self.enx - plx <= -2 or self.eny - ply >= 2 or self.eny - ply <= -2 and self.name != "Ghost":
                if self.los() == True and random.randint(0, 10) <= 3:
                    plhp = self.forskellymagic(plhp)
                    moved = True
            if moved == False:
                foremap[self.enx][self.eny] = ground
                if keepgoskel == 'UP' and self.enx - 1 >= 0:
                    if foremap[self.enx - 1][self.eny] == ground:
                        self.enx -= 1
                        direct = 'UP'
                if keepgoskel == 'DOWN' and self.enx + 1 <= 9:
                    if foremap[self.enx + 1][self.eny] == ground:
                        self.enx += 1
                        direct = 'DOWN'
                if keepgoskel == 'LEFT' and self.eny - 1 >= 0:
                    if foremap[self.enx][self.eny - 1] == ground:
                        self.eny -= 1
                        direct = 'LEFT'
                if keepgoskel == 'RIGHT' and self.eny + 1 <= 9:
                    if foremap[self.enx][self.eny + 1] == ground:
                        self.eny += 1
                        direct = 'RIGHT'
                foremap[self.enx][self.eny] = self.image
                return direct

    def dropitem(self):
        if self.name == "King Pig":
            return getitem(self.enx, self.eny, 0, "Axe of Guinea")
        if random.randint(1, 100) <= 2:
            if self.name == "Goblin":
                return getitem(self.enx, self.eny, 0, "Goblin's Dagger")
            if self.name == "Knight":
                return getitem(self.enx, self.eny, 0, "Knight's Sword")
            if self.name == "Guinea Pig":
                return getitem(self.enx, self.eny, 0, "Axe of Guinea")
        if random.randint(0, 100) <= 10:
            rn = random.randint(1, 100)
            if floor < 5:
                if rn <= 90:
                    return getitem(self.enx, self.eny, 0, "Weak Potion")
                if rn > 90:
                    return getitem(self.enx, self.eny, 0, "Antidote")
            if floor >= 5 and floor < 10:
                if rn <= 25:
                    return getitem(self.enx, self.eny, 0, "Potion")
                if rn > 25 and rn <= 40:
                    return getitem(self.enx, self.eny, 0, "Flash Bomb")
                if rn > 40 and rn <= 55:
                    return getitem(self.enx, self.eny, 0, "Speed Potion")
                if rn > 55 and rn <= 75:
                    return getitem(self.enx, self.eny, 0, "Antidote")
                if rn > 75 and rn <= 95:
                    return getitem(self.enx, self.eny, 0, "Paralysis Heal")
                if rn > 95:
                    return getitem(self.enx, self.eny, 0, "Weak Potion")
            if floor >= 10:
                if rn <= 50:
                    return getitem(self.enx, self.eny, 0, "Strong Potion")
                if rn > 50 and rn <= 60:
                    return getitem(self.enx, self.eny, 0, "Speed Potion")
                if rn > 60 and rn <= 75:
                    return getitem(self.enx, self.eny, 0, "Flash Bomb")
                if rn > 75 and rn <= 80:
                    return getitem(self.enx, self.eny, 0, "Heal All")
                if rn > 80 and rn <= 95:
                    return getitem(self.enx, self.eny, 0, "Potion")
                if rn > 95:
                    return getitem(self.enx, self.eny, 0, "Invincibility Potion")

    def die(self):
        global xp, foremap, backmap
        self.drop = 0
        if self.hp <= 0:
            self.dead = True
            self.loaded = False
            if self.xpused == False:
                xp += self.xp
                self.xpused = True
            if backmap[self.enx][self.eny] == ground:
                self.drop = self.dropitem()
            if self.drop == 0 or self.drop == None:
                foremap[self.enx][self.eny] = backmap[self.enx][self.eny]
            if weapon != "fist":
                updatelog('kill', self.name, weapon.weaptype)
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
                if floor == 10:
                    foremap[9][4] = ground
                    foremap[9][5] = ground
                    foremap[2][4] = downstair
                    backmap[2][4] = downstair

    def recycle(self, stair = False):
        if self.name == "Little-Eagle" and littlespawn == False:
            return
        self.dead = False
        self.hp = self.temphp
        self.xpused = False
        if stair == True:
            self.loaded = False
            self.rmfl = (0, 0)
            self.enx, self.eny = 0, 0
            self.spawnx, self.spawny = 0, 0
            self.currentloc = ((0, 0), (0, 0))
            
#kill me now
#Name, HP, Attack, Armor, Damage, XP, image
enemies = [
#---Floors 1-5---#
Enemy("Goblin", 5, 3, 5, 3, 3, goblin), #0
Enemy("Goblin", 5, 3, 5, 3, 3, goblin),
Enemy("Goblin", 5, 3, 5, 3, 3, goblin),
Enemy("Goblin", 5, 3, 5, 3, 3, goblin),
Enemy("Goblin", 5, 3, 5, 3, 3, goblin),
Enemy("Goblin", 5, 3, 5, 3, 3, goblin),
Enemy("Goblin", 5, 3, 5, 3, 3, goblin),
Enemy("Goblin", 5, 3, 5, 3, 3, goblin),
Enemy("Goblin", 5, 3, 5, 3, 3, goblin),
Enemy("Goblin", 5, 3, 5, 3, 3, goblin),
Enemy("Rat", 3, 2, 6, 2, 2, rat),   #10
Enemy("Rat", 3, 2, 6, 2, 2, rat),
Enemy("Rat", 3, 2, 6, 2, 2, rat),
Enemy("Rat", 3, 2, 6, 2, 2, rat),
Enemy("Rat", 3, 2, 6, 2, 2, rat),
Enemy("Rat", 3, 2, 6, 2, 2, rat),
Enemy("Rat", 3, 2, 6, 2, 2, rat),
Enemy("Rat", 3, 2, 6, 2, 2, rat),
Enemy("Rat", 3, 2, 6, 2, 2, rat),
Enemy("Rat", 3, 2, 6, 2, 2, rat),
Enemy("Snake", 6, 15, 25, 4, 3, snake),   #20
Enemy("Snake", 6, 15, 25, 4, 3, snake),
Enemy("Snake", 6, 15, 25, 4, 3, snake),
Enemy("Snake", 6, 15, 25, 4, 3, snake),
Enemy("Snake", 6, 15, 25, 4, 3, snake),
Enemy("Snake", 6, 15, 25, 4, 3, snake),
Enemy("Snake", 6, 15, 25, 4, 3, snake),
Enemy("Snake", 6, 15, 25, 4, 3, snake),
Enemy("Snake", 6, 15, 25, 4, 3, snake),
Enemy("Snake", 6, 15, 25, 4, 3, snake),
Enemy("Guinea Pig", 6, 15, 20, 4, 4, guinea), #30
Enemy("Guinea Pig", 6, 15, 20, 4, 4, guinea),
Enemy("Guinea Pig", 6, 15, 20, 4, 4, guinea),
Enemy("Guinea Pig", 6, 15, 20, 4, 4, guinea),
Enemy("Guinea Pig", 6, 15, 20, 4, 4, guinea),
Enemy("Guinea Pig", 6, 15, 20, 4, 4, guinea),
Enemy("Guinea Pig", 6, 15, 20, 4, 4, guinea),
Enemy("Guinea Pig", 6, 15, 20, 4, 4, guinea),
Enemy("Guinea Pig", 6, 15, 20, 4, 4, guinea),
Enemy("Guinea Pig", 6, 15, 20, 4, 4, guinea),
#---Floors 6-10---#
Enemy("Megabat", 10, 20, 25, 4, 10, megabat), #40
Enemy("Megabat", 10, 20, 25, 4, 10, megabat),
Enemy("Megabat", 10, 20, 25, 4, 10, megabat),
Enemy("Megabat", 10, 20, 25, 4, 10, megabat),
Enemy("Megabat", 10, 20, 25, 4, 10, megabat),
Enemy("Megabat", 10, 20, 25, 4, 10, megabat),
Enemy("Megabat", 10, 20, 25, 4, 10, megabat),
Enemy("Megabat", 10, 20, 25, 4, 10, megabat),
Enemy("Megabat", 10, 20, 25, 4, 10, megabat),
Enemy("Megabat", 10, 20, 25, 4, 10, megabat),
Enemy("Mammoth", 13, 23, 13, 7, 12, mammoth), #50
Enemy("Mammoth", 13, 23, 13, 7, 12, mammoth),
Enemy("Mammoth", 13, 23, 13, 7, 12, mammoth),
Enemy("Mammoth", 13, 23, 13, 7, 12, mammoth),
Enemy("Mammoth", 13, 23, 13, 7, 12, mammoth),
Enemy("Mammoth", 13, 23, 13, 7, 12, mammoth),
Enemy("Mammoth", 13, 23, 13, 7, 12, mammoth),
Enemy("Mammoth", 13, 23, 13, 7, 12, mammoth),
Enemy("Mammoth", 13, 23, 13, 7, 12, mammoth),
Enemy("Mammoth", 13, 23, 13, 7, 12, mammoth),
Enemy("Monster", 10, 18, 18, 5, 6, monster),  #60
Enemy("Monster", 10, 18, 18, 5, 6, monster),
Enemy("Monster", 10, 18, 18, 5, 6, monster),
Enemy("Monster", 10, 18, 18, 5, 6, monster),
Enemy("Monster", 10, 18, 18, 5, 6, monster),
Enemy("Monster", 10, 18, 18, 5, 6, monster),
Enemy("Monster", 10, 18, 18, 5, 6, monster),
Enemy("Monster", 10, 18, 18, 5, 6, monster),
Enemy("Monster", 10, 18, 18, 5, 6, monster),
Enemy("Monster", 10, 18, 18, 5, 6, monster),
Enemy("Troll", 30, 25, 13, 13, 10, troll2), #70
Enemy("Troll", 30, 25, 13, 13, 10, troll2),
Enemy("Troll", 30, 25, 13, 13, 10, troll2),
Enemy("Troll", 30, 25, 13, 13, 10, troll2),
Enemy("Troll", 30, 25, 13, 13, 10, troll2),
Enemy("Troll", 30, 25, 13, 13, 10, troll2),
Enemy("Troll", 30, 25, 13, 13, 10, troll2),
Enemy("Troll", 30, 25, 13, 13, 10, troll2),
Enemy("Troll", 30, 25, 13, 13, 10, troll2),
Enemy("Troll", 30, 25, 13, 13, 10, troll2),
#---Floors 11-15---#    I can't believe how I actually went through with this crap
Enemy("Knight", 13, 20, 18, 6, 20, knight), #80
Enemy("Knight", 13, 20, 18, 6, 20, knight),
Enemy("Knight", 13, 20, 18, 6, 20, knight),
Enemy("Knight", 13, 20, 18, 6, 20, knight),
Enemy("Knight", 13, 20, 18, 6, 20, knight),
Enemy("Knight", 13, 20, 18, 6, 20, knight),
Enemy("Knight", 13, 20, 18, 6, 20, knight),
Enemy("Knight", 13, 20, 18, 6, 20, knight),
Enemy("Knight", 13, 20, 18, 6, 20, knight),
Enemy("Knight", 13, 20, 18, 6, 20, knight),
Enemy("Ghost", 14, 18, 20, 5, 16, ghost),  #90
Enemy("Ghost", 14, 18, 20, 5, 16, ghost),
Enemy("Ghost", 14, 18, 20, 5, 16, ghost),
Enemy("Ghost", 14, 18, 20, 5, 16, ghost),
Enemy("Ghost", 14, 18, 20, 5, 16, ghost),
Enemy("Ghost", 14, 18, 20, 5, 16, ghost),
Enemy("Ghost", 14, 18, 20, 5, 16, ghost),
Enemy("Ghost", 14, 18, 20, 5, 16, ghost),
Enemy("Ghost", 14, 18, 20, 5, 16, ghost),
Enemy("Ghost", 14, 18, 20, 5, 16, ghost),
Enemy("Skeleton", 50, 25, 5, 4, 20, skeleton2), #100
Enemy("Skeleton", 50, 25, 5, 4, 20, skeleton2),
Enemy("Skeleton", 50, 25, 5, 4, 20, skeleton2),
Enemy("Skeleton", 50, 25, 5, 4, 20, skeleton2),
Enemy("Skeleton", 50, 25, 5, 4, 20, skeleton2),
Enemy("Skeleton", 50, 25, 5, 4, 20, skeleton2),
Enemy("Skeleton", 50, 25, 5, 4, 20, skeleton2),
Enemy("Skeleton", 50, 25, 5, 4, 20, skeleton2),
Enemy("Skeleton", 50, 25, 5, 4, 20, skeleton2),
Enemy("Skeleton", 50, 25, 5, 4, 20, skeleton2),
Enemy("Little-Eagle", 15, 30, 15, 4, 18, littleeagle),   #110
Enemy("Little-Eagle", 15, 30, 15, 4, 18, littleeagle),
Enemy("Little-Eagle", 15, 30, 15, 4, 18, littleeagle),
Enemy("Little-Eagle", 15, 30, 15, 4, 18, littleeagle),
Enemy("Little-Eagle", 15, 30, 15, 4, 18, littleeagle),
Enemy("Little-Eagle", 15, 30, 15, 4, 18, littleeagle),
Enemy("Little-Eagle", 15, 30, 15, 4, 18, littleeagle),
Enemy("Little-Eagle", 15, 30, 15, 4, 18, littleeagle),
Enemy("Little-Eagle", 15, 30, 15, 4, 18, littleeagle),
Enemy("Little-Eagle", 15, 30, 15, 4, 18, littleeagle)
]

bosses = [
Enemy("Troll", 30, 25, 13, 13, 30, troll),
Enemy("Skeleton", 75, 25, 5, 4, 80, skeleton),
Enemy("Big-Eagle", 200, 30, 6, 10, 0, bigeagle),
Enemy("King Pig", 250, 15, 5, 20, 300, kingpig)
]

#good luck figuring what this does
def getrandmon():
    rn = random.randint(1, 100)
    if floor <= 5:
        if rn <= 25:
            return 0
        if rn > 25 and rn <= 50:
            return 10
        if floor == 3:
            if rn > 50 and rn <= 75:
                return 30
            if rn > 75 and rn <= 88:
                return 0
            if rn > 88:
                return 10
        if floor > 3 and floor <= 5:
            if rn > 50 and rn <= 75:
                return 20
            if rn > 75:
                return 30
        if rn > 50 and rn <= 75:
            return 0
        if rn > 75:
            return 10
    if floor > 5 and floor <= 10:
        if rn <= 25:
            return 40
        if rn > 25 and rn <= 50:
            return 50
        if floor == 8:
            if rn > 50 and rn <= 75:
                return 60
            if rn > 75 and rn <= 88:
                return 40
            if rn > 88:
                return 50
        if floor > 8 and floor <= 10:
            if rn > 50 and rn <= 75:
                return 60
            if rn > 75:
                return 70
        if rn > 50 and rn <= 75:
            return 40
        if rn > 75:
            return 50 
    if floor > 10:
        if rn <= 25:
            return 80
        if rn > 25 and rn <= 50:
            return 90
        if floor == 13:
            if rn > 50 and rn <= 75:
                return 100
            if rn > 75 and rn <= 88:
                return 80
            if rn > 88:
                return 90
        if floor > 13:
            if rn > 50 and rn <= 75:
                return 100
            if rn > 75:
                return 110
        if rn > 50 and rn <= 75:
            return 80
        if rn > 75:
            return 90

def getmon(x, y, kind = 0):
            
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

    if kind != 0:
        if enemies[kind].dead == False and enemies[kind].currentloc == ((0, 0), (0, 0)):
            enemies[kind].image = pygame.image.load('graphics/guinea2.png').convert()
            enemies[kind].enx = x
            enemies[kind].eny = y
            enemies[kind].spawnx, enemies[kind].spawny = x, y
            enemies[kind].loaded = True
            enemies[kind].rmfl = (room, floor)
            enemies[kind].currentloc = ((room, floor), (x, y))
            updatelog('view', enemies[kind].name)
            return enemies[kind].image

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
    global finalset
    if fl == 5:
        num = 0
    if fl == 10:
        num = 1
    if fl == 15 and room != 9:
        num = 2
        if finalset == True:
            return ground
        bosses[num].stage = 1
        bosses[num].enroom = room
        finalset = True
    if fl == 15 and room == 9:
        num = 3
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

def checkstage():
    if bosses[2].hp <= 125:
        bosses[2].stage = 2 
    if bosses[2].hp <= 50:
        bosses[2].stage = 3

def getitem(x, y, kind, bagkind = 0):

    swordlow = Item("Iron Sword", 'WEAP', 2, treasure, 6, 'sword')
    swordmed = Item("Steel Sword", 'WEAP', 4, treasure, 8, 'sword')
    swordhigh = Item("Platinum Sword", 'WEAP', 6, treasure, 10, 'sword')
    daggerlow = Item("Iron Dagger", 'WEAP', 4, treasure, 4, 'dagger')
    daggermed = Item("Steel Dagger", 'WEAP', 6, treasure, 6, 'dagger')
    daggerhigh = Item("Platinum Dagger", 'WEAP', 8, treasure, 8, 'dagger')
    axelow = Item("Iron Axe", 'WEAP', 0, treasure, 8, 'axe')
    axemed = Item("Steel Axe", 'WEAP', 2, treasure, 10, 'axe')
    axehigh = Item("Platinum Axe", 'WEAP', 4, treasure, 12, 'axe')

    swordsp = Item("Knight's Sword", 'WEAP', 8, treasure, 10, 'sword')
    daggersp = Item("Goblin's Dagger", 'WEAP', 10, treasure, 8, 'dagger')
    axesp = Item("Axe of Guinea", 'WEAP', 4, treasure, 14, 'axe')

    armorlow = Item("Iron Armor", 'ARM', 3, treasure)
    armormed = Item("Steel Armor", 'ARM', 6, treasure)
    armorhigh = Item("Platinum Armor", 'ARM', 9, treasure)

    weakpot = Item("Weak Potion", 'HEAL', 5, bag)
    pot = Item("Potion", 'HEAL', 20, bag)
    strpot = Item("Strong Potion", 'HEAL', 40, bag)
    ant = Item("Antidote", 'PSN', 0, bag)
    paraheal = Item("Paralysis Heal", 'PARA', 0, bag)
    healall = Item("Heal All", 'ALL', 0, bag)
    speed = Item("Speed Potion", 'SPD', 0, bag)
    invpot = Item("Invincibility Potion", 'INV', 0, bag)
    flashbomb = Item("Flash Bomb", 'FLSH', 0, bag)

    if bagkind != 0: #for drops
        if bagkind == "Weak Potion":
            tempitem = weakpot
        if bagkind == "Antidote":
            tempitem = ant
        if bagkind == "Strong Potion":
            tempitem = strpot
        if bagkind == "Potion":
            tempitem = pot
        if bagkind == "Paralysis Heal":
            tempitem = paraheal
        if bagkind == "Speed Potion":
            tempitem = speed
        if bagkind == "Invincibility Potion":
            tempitem = invpot
        if bagkind == "Flash Bomb":
            tempitem = flashbomb
        if bagkind == "Heal All":
            tempitem = healall
        if bagkind == "Flash Bomb":
            tempitem = flashbomb
        if bagkind == "Goblin's Dagger":
            tempitem = daggersp
        if bagkind == "Knight's Sword":
            tempitem = swordsp
        if bagkind == "Axe of Guinea":
            tempitem = axesp
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
            if rn <= 80:
                tempitem = weakpot
            if rn > 80:
                tempitem = ant
        if floor > 2 and floor <= 5:
            if rn <= 30:
                tempitem = weakpot
            if rn > 30 and rn <= 60:
                tempitem = pot
            if rn > 60 and rn <= 80:
                tempitem = ant
            if rn > 80:
                tempitem = paraheal
        if floor >= 6 and floor < 10:
            if rn <= 50:
                tempitem = pot
            if rn > 50 and rn <= 65:
                tempitem = flashbomb
            if rn > 65 and rn <= 75:
                tempitem = speed
            if rn > 75 and rn <= 85:
                tempitem = healall
            if rn > 85:
                tempitem = pot
        if floor >= 10:
            if rn <= 50:
                tempitem = strpot
            if rn > 50 and rn <= 60:
                tempitem = speed
            if rn > 60 and rn <= 75:
                tempitem = flashbomb
            if rn > 75 and rn <= 80:
                tempitem = healall
            if rn > 80 and rn <= 95:
                tempitem = pot
            if rn > 95:
                tempitem = invpot
    tempitem.pos = (x, y)
    tempitem.rmfl = (room, floor)
    additem(items, tempitem)
    return tempitem.image

def keystatus():
    global haskey
    numkey = 0
    for i in range(len(haskey)):
        if haskey[i] != 0:
            numkey += 1
    if numkey == 0:
        screen.fill(pygame.Color("black"), (480, 550, 15, 15))   
        screen.fill(pygame.Color("black"), (450, 500, 50, 50))
    else:
        screen.blit(log.render(str(numkey), True, pygame.Color("white")), (485, 550))
        screen.blit(keyinv, (450, 500))

def pickup():
    global keypos, haskey, invmax, itemrmflxy
    for i in range(len(haskey)):
        if (plx, ply) == keypos and haskey[i] == 0:
            haskey[i] = floor
            keyused.append((room, floor))
            foremap[plx][ply] = player 
            backmap[plx][ply] = ground
            updatelog('pick', "key")
            keystatus()
            return
    for i in range(len(items)):
        if items[i].pos == (plx, ply) and items[i].rmfl == (room, floor) and invmax + 1 <= invmaxmax:
            items[i].ininv = True
            if items[i].dropped == False:
                rmflxy = (items[i].rmfl, items[i].pos)
                itemrmflxy.append(rmflxy)
            items[i].pos = (0, 0)
            backmap[plx][ply] = ground
            invmax += 1
            updatelog('pick', items[i].name)
        else:
            updatelog('invmax')

def openinv(itemslist):
    curschar = log.render(">", True, pygame.Color("white"))
    col = 0
    row = 0
    rowmin = 0
    colmin = 0
    rowmax = 8
    colmax = 1
    log.set_underline(True)
    #any easier way?
    textatt = log.render("Att", True, pygame.Color("blue"))
    textslash = log.render("/", True, pygame.Color("white"))
    textheal = log.render("Heal", True, pygame.Color("yellow"))
    textdam = log.render("Dam", True, pygame.Color("red"))
    log.set_underline(False)
    while True:
        screen.fill(pygame.Color("black"), (0, 0, 500, 500))
        screen.blit(textatt, (171, 25))
        screen.blit(textslash, (195, 25))
        screen.blit(textheal, (203, 25))
        screen.blit(textdam, (245, 25))
        tempinvitems = iteminv(itemslist)
        itemslist = restorelistpos(itemslist)
        if tempinvitems != None:
            invitems = sorted(tempinvitems, key=lambda tempinvitems: tempinvitems.weaptype, reverse=True)

        if tempinvitems != None:
            j = 0
            for i in range(len(invitems)):
                if i > rowmax:  #>=?
                    j = 1
                    invitems[i].row = i - 9
                if j != 1:
                    invitems[i].row = i
                invitems[i].col = j

            for i in range(len(invitems)):
                slot = (50 + (260 * invitems[i].col), 60 + (50 * invitems[i].row))
                if invitems[i].kind == 'WEAP' or invitems[i].kind == 'ARM':
                    screen.blit(log.render(invitems[i].name, True, pygame.Color("blue")), slot)
                    screen.blit(log.render(str(invitems[i].value), True, pygame.Color("blue")), (200 + (260 * invitems[i].col), 60 + (50 * invitems[i].row)))
                    if invitems[i].equip == True:
                        screen.blit(log.render("*", True, pygame.Color("blue")), (42 + (260 * invitems[i].col), 62 + (50 * invitems[i].row)))
                    else:
                        screen.fill(pygame.Color("black"), (40 + (260 * invitems[i].col), 60 + (50 * invitems[i].row), 5, 5))
                if invitems[i].kind == 'WEAP':
                    screen.blit(log.render(str(invitems[i].damage), True, pygame.Color("red")), (250 + (260 * invitems[i].col), 60 + (50 * invitems[i].row)))
                if invitems[i].kind == 'HEAL':
                    screen.blit(log.render(invitems[i].name, True, pygame.Color("yellow")), slot)
                    screen.blit(log.render(str(invitems[i].value), True, pygame.Color("yellow")), (200 + (260 * invitems[i].col), 60 + (50 * invitems[i].row)))
                else:
                    screen.blit(log.render(invitems[i].name, True, pygame.Color("white")), slot)

        screen.blit(curschar, (35 + (260 * col), 60 + (50 * row)))

        pygame.display.update()

        select = pygame.event.wait()
        screen.fill(pygame.Color("black"), (30 + (260 * col), 50 + (50 * row), 10, 10))
        if select.type == pygame.QUIT:
            sys.exit()
        elif select.type == pygame.KEYDOWN:
            if select.key == pygame.K_UP and row - 1 >= rowmin:
                row -= 1
            if select.key == pygame.K_DOWN and row + 1 <= rowmax:
                row += 1
            if select.key == pygame.K_LEFT and col - 1 >= colmin:
                col -= 1
            if select.key == pygame.K_RIGHT and col + 1 <= colmax:
                col += 1
            if select.key == pygame.K_RETURN:
                for i in range(len(invitems)):
                    if col == invitems[i].col and row == invitems[i].row:
                        invitems[i].use()
            if select.key == pygame.K_d:
                for i in range(len(invitems)):
                    if col == invitems[i].col and row == invitems[i].row:
                        invitems[i].drop()
            if select.key == pygame.K_i:
                return

def attack(enemy, weapon):
    rn = random.randint(1, 20) #d20

    if enemy.ghostinv == False:
        if weapon == "fist":
            if rn + platt > enemy.armor:
                dam = random.randint(1, 3)
                updatelog('att', enemy.name, dam)
                return enemy.hp - dam
            else:
                updatelog('miss', enemy.name)
                return enemy.hp

        if rn + weapon.value + platt > enemy.armor:
            dam = random.randint(1, weapon.damage)
            updatelog('att', enemy.name, dam)
            return enemy.hp - dam
        else:
            updatelog('miss', enemy.name)
            return enemy.hp

def loadmusic(num):
    global bgm
    pygame.time.wait(500)
    screen.fill(pygame.Color("black"), (0, 0, 500, 500))
    pygame.display.update()
    bgm = pygame.mixer.Sound('music/BGM' + str(num) + '.ogg')
    bgm.play(-1, 0, 1000)
    pygame.event.clear()

#load in another map file and display it on the screen
def loadmap(direct):
    global foremap, backmap, plx, ply, floor, room, upstrpos, downstrpos, keypos, loadedroom, wall, ground, player, bag, treasure, key, flash, flashcount, flashmax, door, bossstart, upstair, downstair, statue
    upstrpos = (0, 0)
    downstrpos = (0, 0)
    keypos = (0, 0)
    temp = False
    loadedroom = True
    flash = False
    flashcount = 0
    flashmax = 0

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
        if floor == 5:
            bgm.fadeout(1000)
            loadmusic(1)
        if floor == 10:
            bgm.fadeout(1000)
            loadmusic(2)
        for i in range(len(enemies)):
            enemies[i].recycle(True)
    if direct == 'STAIR_DOWN':
        downstrpos = (0, 0)
        floor += 1
        if floor == 6:
            bgm.fadeout(1000)
            loadmusic(2)
        if floor == 11:
            bgm.fadeout(1000)
            loadmusic(3)
        for i in range(len(enemies)):
            enemies[i].recycle(True)
    if multiroomboss == True and room == bosses[2].enroom:
        bosses[2].loaded = True

    if (floor, room) == (5, 2) and direct == 'RIGHT' and bosses[0].dead == False:
        ply = 1
        updatelog('bossdoor')
    if (floor, room) == (10, 1) and direct == 'UP' and bosses[1].dead == False:
        plx = 8
        updatelog('bossdoor')
    if (floor, room) == (15, 5) and bossstart == False:
        plx = 8
        updatelog('bossdoor')
        bossstart = True

    if floor <= 5:
        wall = pygame.image.load('graphics/wall.png').convert()
        ground = pygame.image.load('graphics/ground.png').convert()
        statue = pygame.image.load('graphics/statue.png').convert()
        player = pygame.image.load('graphics/player.png').convert()
        bag = pygame.image.load('graphics/bag.png').convert()
        treasure = pygame.image.load('graphics/treasure.png').convert()
        key = pygame.image.load('graphics/key.png').convert()
        upstair = pygame.image.load('graphics/upstair.png').convert()
        downstair = pygame.image.load('graphics/downstair.png').convert()
    if floor > 5 and floor <= 10:
        wall = pygame.image.load('graphics/wall2.png').convert()
        ground = pygame.image.load('graphics/ground2.png').convert()
        statue = pygame.image.load('graphics/statue2.png').convert()
        player = pygame.image.load('graphics/player2.png').convert()
        bag = pygame.image.load('graphics/bag2.png').convert()
        treasure = pygame.image.load('graphics/treasure2.png').convert()
        key = pygame.image.load('graphics/key2.png').convert()
        door = pygame.image.load('graphics/door2.png').convert()
        upstair = pygame.image.load('graphics/upstair2.png').convert()
        downstair = pygame.image.load('graphics/downstair2.png').convert()
    if floor > 10:
        wall = pygame.image.load('graphics/wall3.png').convert()
        ground = pygame.image.load('graphics/ground3.png').convert()
        statue = pygame.image.load('graphics/statue3.png').convert()
        player = pygame.image.load('graphics/player3.png').convert()
        bag = pygame.image.load('graphics/bag3.png').convert()
        treasure = pygame.image.load('graphics/treasure3.png').convert()
        key = pygame.image.load('graphics/key3.png').convert()
        door = pygame.image.load('graphics/door3.png').convert()
        upstair = pygame.image.load('graphics/upstair3.png').convert()
        downstair = pygame.image.load('graphics/downstair3.png').convert()

    newmap = "rooms/fl" + str(floor) + "r" + str(room) + ".txt"
    newmap = open(newmap, 'r')
    newmap = newmap.read()
    newmap = newmap.replace('\n' , '')

    for i in range(10):
        for j in range(10):
            backmap[i][j] = newmap[i * 10 + j]

    count = 30
    for i in range(10):
        for j in range(10):

            for k in range(len(items)): #for items that were dropped
                if (i, j) == items[k].pos and (room, floor) == items[k].rmfl:
                    foremap[i][j] = items[k].image
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
            if backmap[i][j] == 'E' and floor != 15:
                foremap[i][j] = getmon(i, j)
                backmap[i][j] = ground
            if backmap[i][j] == 'E' and floor == 15:
                foremap[i][j] = getmon(i, j, count)
                backmap[i][j] = ground
                count += 1
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
                    updatelog('view', "key")
                else:
                    foremap[i][j] = ground
                    backmap[i][j] = ground
            if backmap[i][j] == 'D':
                for k in range(len(dooropen)):
                    if dooropen[k] != (room, floor):
                        foremap[i][j] = door
                    else:
                        foremap[i][j] = ground
                        break
                backmap[i][j] = ground
            if backmap[i][j] == 'T':
                tracker = 0
                for k in range(len(itemrmflxy)):
                    if ((room, floor), (i, j)) == itemrmflxy[k]:
                        tracker += 1
                if tracker == 0:
                    foremap[i][j] = getitem(i, j, 'T')
                    updatelog('view', "treasure chest")
                else:
                    foremap[i][j] = ground
                backmap[i][j] = foremap[i][j]
            if backmap[i][j] == 'B':
                tracker = 0
                for k in range(len(itemrmflxy)):
                    if ((room, floor), (i, j)) == itemrmflxy[k]:
                        tracker += 1
                if tracker == 0:
                    foremap[i][j] = getitem(i, j, 'B')
                    updatelog('view', "bag")
                else:
                    foremap[i][j] = ground
                backmap[i][j] = foremap[i][j]
            if backmap[i][j] == '<':
                foremap[i][j] = upstair
                backmap[i][j] = upstair
                upstrpos = (i, j)
                updatelog('view', "staircase")
            if backmap[i][j] == '>':
                foremap[i][j] = downstair
                backmap[i][j] = downstair
                downstrpos = (i, j)
                updatelog('view', "staircase")
    if (room, floor) == (1, 10):
        downstrpos = (2, 4)

    screen.fill(pygame.Color("black"), (450, 585, 50, 15))
    screen.blit(log.render("FL: " + str(floor), True, pygame.Color("white")), (450, 585))

#it's terrible, I know
def move(x):
    global foremap, plx, ply, haskey, dooropen

    if para == True:
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

        if foremap[plx - 1][ply] == door:
            for i in range(len(haskey)):
                keyflag = 0
                if haskey[i] == floor:
                    foremap[plx - 1][ply] = backmap[plx - 1][ply]
                    haskey[i] = 0
                    dooropen.append((room, floor))
                    keystatus()
                    return
                else:
                    keyflag += 1
            if keyflag == 4:
                updatelog('wrongkey')
                return
            updatelog('nokey')

        if foremap[plx - 1][ply] != wall and foremap[plx - 1][ply] != statue and foremap[plx - 1][ply] != door and load == False and attacked == False:
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

        #I only put this in the LEFT and UP, sue me
        if foremap[plx][ply - 1] == door:
            keyflag = 0
            for i in range(len(haskey)):
                if haskey[i] == floor:
                    foremap[plx][ply - 1] = backmap[plx][ply - 1]
                    haskey[i] = 0
                    dooropen.append((room, floor))
                    keystatus()
                    return
                else:
                    keyflag += 1
            if keyflag == 4:
                updatelog('wrongkey')
                return
            updatelog('nokey')

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
        elif backmap[plx][ply] == upstair:
            loadmap('STAIR_UP')

    if x == 'STAIR_DOWN':
        if (plx, ply) == downstrpos:
            loadmap('STAIR_DOWN')
        elif backmap[plx][ply] == downstair:
            loadmap('STAIR_DOWN')

    foremap[plx][ply] = player

def winner():
    for k in range(255, 0, -1):
        screen.fill(pygame.Color("black"), (0, 0, 500, 500))
        for i in range(10):
            for j in range(10):
                foremap[i][j].convert_alpha()
                foremap[i][j].set_alpha(k)
                screen.blit(foremap[i][j], (j * 50, i * 50))
        pygame.display.update()
        pygame.time.wait(10)
    screen.fill(pygame.Color("black"), (0, 0, 500, 500))
    pygame.time.wait(2000)
    screen.blit(big.render("YOU WIN", True, pygame.Color("green")), (150, 200))
    updatelog('win')
    pygame.display.update()
    pygame.time.wait(3000)
    screen.fill(pygame.Color("black"), (0, 0, 500, 500))
    screen.blit(med.render("Programming", True, pygame.Color("white")), (155, 50))
    screen.blit(med.render("Conner Dreher", True, pygame.Color("white")), (135, 100))
    screen.blit(med.render("Everything Else", True, pygame.Color("white")), (130, 200))
    screen.blit(med.render("Dan Oniones", True, pygame.Color("white")), (160, 250))
    pygame.display.update()
    pygame.time.wait(3000)
    pygame.event.clear()
    pygame.event.wait()
    sys.exit()

#main game loop     this is by far the most messy place in here
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
            openinv(items)
        if event.key == pygame.K_COMMA:
            pickup()
        if event.key == pygame.K_a:
            floor = 11
            room = 0
        if event.key == pygame.K_r:
            xp += 10

    if pygame.mixer.get_busy() == False:
        if floor <= 5:
            loadmusic(1)
        if floor > 5 and floor <= 10:
            loadmusic(2)
        if floor > 10:
            loadmusic(3)

    if flash == True and flashmax == 0:
        flashtemp = 0
        for i in range(len(enemies)):
            if enemies[i].loaded == True:
                flashtemp += 1
        flashmax = flashtemp * 10

    if event.key != pygame.K_i and event.key != pygame.K_COMMA:
        if speedcount >= 10:
            speed = False
            speedcount = 0
            speedturn = 0

        if floor == 15 and room != 7 and room != 8 and room != 9:
            multiroomboss = True
            if loadedroom == False:
                littlespawn = False
            else:
                littlespawn = True

        if loadedroom == True and multiroomboss == True and bosses[2].dead == False and bosses[2].enroom == room:   #and and and and and
            bosses[2].enx = 4
            bosses[2].eny = 4
            updatelog("telein", bosses[2].name)
        if loadedroom == True and multiroomboss == True and bosses[2].dead == False and bosses[2].stage == 1: #oh gosh
            bosses[2].enx = 4
            bosses[2].eny = 4
            updatelog("telein", bosses[2].name) #now this is what I call cutting corners
        if bosses[2].enroom > 6 or bosses[2].enroom < 1 and multiroomboss == True:
            bosses[2].enroom = 5

        if speed == False or speedturn == 1:
            speedcount += 1
            speedturn = 0
            for i in range(len(enemies)):
                enemies[i].die()
                if enemies[i].name == "Ghost" and enemies[i].hp <= 6  and enemies[i].dead == False and enemies[i].loaded == True:
                    tempskelgo = skelgo
                    skelgo = enemies[i].forskellyonly(tempskelgo)
                    if enemies[i].invcount == 0:
                        enemies[i].ghostinv = True
                    if enemies[i].ghostinv == True:
                        enemies[i].invcount += 1
                    if enemies[i].invcount == 3:
                        enemies[i].ghostinv = False #what was I thinking?
                if enemies[i].name == "Skeleton" and enemies[i].loaded == True:
                    tempskelgo = skelgo
                    skelgo = enemies[i].forskellyonly(tempskelgo)
                if enemies[i].dead == False:
                    tempgo = enemies[i].keepgo
                    enemies[i].keepgo = enemies[i].enmv(tempgo)
                    if enemies[i].name == "Megabat":
                        tempgo = enemies[i].keepgo
                        enemies[i].keepgo = enemies[i].enmv(tempgo)
                else:
                    if enemies[i].drop != None and enemies[i].drop != 0:
                        foremap[enemies[i].enx][enemies[i].eny] = enemies[i].drop
                        backmap[enemies[i].enx][enemies[i].eny] = enemies[i].drop
                    screen.blit(foremap[enemies[i].enx][enemies[i].eny], (enemies[i].enx * 50, enemies[i].eny * 50))
                    screen.blit(wall, (0, 0)) #this and all the other wall blits at 0,0 are there because I got mad at the split second appearence of dead enemies in that spot
                    pygame.display.update() #and I don't know which one fixed it and I don't want to test it over and over
                    enemies[i].enx, enemies[i].eny = 0, 0
                    enemies[i].recycle()
            for i in range(len(bosses)):
                bosses[i].die()
                checkstage()
                #I've given up at this point    look at all those useless ands
                if bosses[i].dead == False and bosses[i].name == "Big-Eagle" and bosses[i].enroom != room and bosses[i].stage >= 2 and bosses[i].teleported == True:
                    if telecount % 3 == 0:
                        for j in range(110, 114):
                            if j == 110 and plx + 2 < 10 and ply + 2 < 10 and foremap[plx + 2][ply + 2] == ground:
                                enemies[j].enx = plx + 2
                                enemies[j].eny = ply + 2
                                enemies[j].spawnx, enemies[j].spawny = plx + 2, ply + 2
                            if j == 111 and plx - 2 >= 0 and ply - 2 >= 0 and foremap[plx - 2][ply - 2] == ground:
                                enemies[j].enx = plx - 2
                                enemies[j].eny = ply - 2
                                enemies[j].spawnx, enemies[j].spawny = plx - 2, ply - 2
                            if j == 112 and plx + 2 < 10 and ply - 2 >= 0 and foremap[plx + 2][ply - 2] == ground:    #why
                                enemies[j].enx = plx + 2
                                enemies[j].eny = ply - 2
                                enemies[j].spawnx, enemies[j].spawny = plx + 2, ply - 2
                            if j == 113 and plx - 2 >= 0 and ply + 2 < 10 and foremap[plx - 2][ply + 2] == ground:
                                enemies[j].enx = plx - 2
                                enemies[j].eny = ply + 2
                                enemies[j].spawnx, enemies[j].spawny = plx - 2, ply + 2
                            enemies[j].loaded = True
                            enemies[j].rmfl = (room, floor)
                            enemies[j].currentloc = ((room, floor), (enemies[j].enx, enemies[j].eny))
                        updatelog('sur', enemies[110].name)
                    telecount += 1
                    bosses[i].loaded = False
                    bosses[i].teleported = False
                if (bosses[i].loaded == True and bosses[i].dead == False) and ((bosses[i].name != "Skeleton" and bosses[i].name != "Big-Eagle") or bosses[i].stage == 3):
                    tempgo = bosses[i].keepgo
                    bosses[i].keepgo = bosses[i].enmv(tempgo)
                elif bosses[i].loaded == True and bosses[i].dead == False:
                    tempskelgo = skelgo
                    skelgo = bosses[i].forskellyonly(tempskelgo)
                else:
                    if bosses[i].drop != None and bosses[i].drop != 0:
                        foremap[bosses[i].enx][bosses[i].eny] = bosses[i].drop
                        backmap[bosses[i].enx][bosses[i].eny] = bosses[i].drop
                    screen.blit(foremap[bosses[i].enx][bosses[i].eny], (bosses[i].enx * 50, bosses[i].eny * 50))
                    screen.blit(wall, (0, 0))
                    pygame.display.update()
                    bosses[i].enx, bosses[i].eny = 0, 0
        elif speed == True:
            speedturn += 1

        foremap[plx][ply] = player #makes it so you don't go invisible on a tile a monster died on
        foremap[0][0] = wall

        screen.fill(pygame.Color("black"), (25, 500, 23, 15))
        screen.fill(pygame.Color("black"), (75, 500, 110, 15))
        screen.fill(pygame.Color("black"), (229, 500, 20, 15))
        screen.fill(pygame.Color("black"), (299, 500, 20, 15))
        screen.blit(log.render(str(plhp), True, pygame.Color("white")), (32, 500)) #the weird number is used just to keep the value in the same place
        screen.blit(log.render("XP: " + str(xp) + "/" + str(nextlvl[level]), True, pygame.Color("white")), (80, 500))
        if weapon == "fist":
            screen.blit(log.render(str(platt), True, pygame.Color("white")), (230, 500))
        else:
            screen.blit(log.render(str(platt + weapon.value), True, pygame.Color("white")), (230, 500))
        screen.blit(log.render(str(armor), True, pygame.Color("white")), (300, 500))

        if psn == True:
            screen.blit(log.render("PSN", True, pygame.Color("purple")), (325, 500))
            if psnstep % 10 == 0:
                plhp -= 1
                updatelog('psn')
            if psnstep >= 100:
                psn = False
                updatelog('psnheal')
            psnstep += 1
        if para == True:
            screen.blit(log.render("PARA", True, pygame.Color("red")), (355, 500))
            updatelog('para')
            paracount += 1
            if paracount >= paramax:
                para = False
                updatelog('paraheal2')
                paracount = 0
        if nodam == True:
            screen.blit(log.render("INV", True, pygame.Color("yellow")), (420, 500))
            nodamcount += 1
            if nodamcount == 5:
                screen.fill(pygame.Color("black"), (419, 500, 30, 15))
                nodam = False
                nodamcount = 0
        if speed == True:
            screen.blit(log.render("SPD", True, pygame.Color("cyan")), (390, 500))
        if speed == False:
            screen.fill(pygame.Color("black"), (389, 500, 30, 15))
        if psn == False:
            screen.fill(pygame.Color("black"), (324, 500, 30, 15))
        if para == False:
            screen.fill(pygame.Color("black"), (354, 500, 45, 15))

        if plhp <= 0:
            updatelog('dead')
            screen.fill(pygame.Color("black"), (0, 0, 500, 500))
            screen.blit(big.render("GAME OVER", True, pygame.Color("red")), (120, 200))
            pygame.display.update()
            pygame.time.wait(1000)
            event = pygame.event.wait()
            sys.exit()
        if bosses[2].dead == True:
            winner()

        foremap[0][0] = wall
        backmap[0][0] = wall
        screen.blit(wall, (0, 0))
        pygame.display.update()
        loadedroom = False

    for i in range(10):
        for j in range(10):
            screen.blit(foremap[i][j], (j * 50, i * 50))
    level = levelup(nextlvl[level])
    keystatus()
    pygame.display.update()
