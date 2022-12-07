from cmu_112_graphics import *
from gameObjects import *
from terrain import *
import random
import time
import math
import copy
import statistics

def appStarted(app):
    app.dimensions = (900, 400)
    app.mapSize = 8500
    app.scrollX = 0 
    app.scrollY = 0
    app.scrollMargin = 250
    app.scrollMarginY = 70
    app.timerDelay = 5
    app.maxSpeed = 4
    app.gravity = -0.5 # jump height is 138 with -0.5 gravity and 12 jump
    app.terrain = []
    app.mudPatches = []
    app.vines = []
    app.onVine = False
    app.onMud = False
    app.enemies = []
    app.powerUpTypes = {'blue': 3,
                        'yellow': 1,
                        'purple': 3,
                        'orange': 7}
    app.powerUps = []
    app.items = []
    app.projectiles = []
    app.ammo = 0
    app.numberOfHoles = 8
    app.holes = createHoles(1200, app.mapSize-300, app.numberOfHoles, 500) #start, stop, amount, margin
    app.numberOfPlatforms = 20
    app.platformLocations = createPlatforms(1200, app.mapSize-500, app.numberOfPlatforms, 
                                            240, -70, 130) #start, stop, amount, low, high, yRange
    app.platforms = []
    app.hero = Character(55, 40, [app.scrollMargin, 0.7*app.height])
    app.lives = 9
    app.timePassed = 0
    app.timeLimit = 100
    app.deathTimer = 0
    app.damageTaken = False
    app.gameOver = False
    app.victory = False
    app.startGame = True
    app.tutorial = False
    app.background = scaleImage(app, app.loadImage('term project/images/background.jpg'), app.dimensions) #https://www.freepik.com/premium-vector/pixel-art-sky-background-with-clouds-cloudy-blue-sky-vector-8bit-game-white-background_26733992.htm
    app.sprite1 = scaleImage(app, app.loadImage('term project/images/pusheen1.png'), (120, 320)) #https://tenor.com/view/pusheen-running-cat-cute-chase-gif-16501897
    app.sprite2 = scaleImage(app, app.loadImage('term project/images/pusheen2.png'), (120, 320))
    app.sprite3 = scaleImage(app, app.loadImage('term project/images/pusheen3.png'), (120, 320))
    app.sprite4 = scaleImage(app, app.loadImage('term project/images/pusheen4.png'), (120, 320))
    # https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#spritesheetsWithCropping
    app.sprites = []
    app.sprites.extend([app.sprite1, app.sprite2, app.sprite3, app.sprite4])
    app.giant = False
    app.giantSprite1 = scaleImage(app, app.loadImage('term project/images/pusheen1.png'), (180, 480)) #https://tenor.com/view/pusheen-running-cat-cute-chase-gif-16501897
    app.giantSprite2 = scaleImage(app, app.loadImage('term project/images/pusheen2.png'), (180, 480))
    app.giantSprite3 = scaleImage(app, app.loadImage('term project/images/pusheen3.png'), (180, 480))
    app.giantSprite4 = scaleImage(app, app.loadImage('term project/images/pusheen4.png'), (180, 480))
    app.giantSprites = []
    app.giantSprites.extend([app.giantSprite1, app.giantSprite2, app.giantSprite3, app.giantSprite4])
    app.fast = False
    app.fastSprite1 = scaleImage(app, app.loadImage('term project/images/fast1.png'), (120, 320)) 
    app.fastSprite2 = scaleImage(app, app.loadImage('term project/images/fast2.png'), (120, 320))
    app.fastSprite3 = scaleImage(app, app.loadImage('term project/images/fast3.png'), (120, 320))
    app.fastSprite4 = scaleImage(app, app.loadImage('term project/images/fast4.png'), (120, 320))
    app.fastSprites = []
    app.fastSprites.extend([app.fastSprite1, app.fastSprite2, app.fastSprite3, app.fastSprite4])
    app.reversed1 = app.sprite1.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    app.reversed2 = app.sprite2.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    app.reversed3 = app.sprite3.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    app.reversed4 = app.sprite4.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    app.reversedSprites = []
    app.reversedSprites.extend([app.reversed1, app.reversed2, app.reversed3, app.reversed4])
    app.giantReversed1 = app.giantSprite1.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    app.giantReversed2 = app.giantSprite2.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    app.giantReversed3 = app.giantSprite3.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    app.giantReversed4 = app.giantSprite4.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    app.reversedGiantSprites = []
    app.reversedGiantSprites.extend([app.giantReversed1, app.giantReversed2, app.giantReversed3, app.giantReversed4])
    app.fastReversed1 = app.fastSprite1.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    app.fastReversed2 = app.fastSprite2.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    app.fastReversed3 = app.fastSprite3.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    app.fastReversed4 = app.fastSprite4.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    app.reversedFastSprites = []
    app.reversedFastSprites.extend([app.fastReversed1, app.fastReversed2, app.fastReversed3, app.fastReversed4])
    app.giantFast1 = scaleImage(app, app.loadImage('term project/images/fast1.png'), (180, 480)) #https://tenor.com/view/pusheen-running-cat-cute-chase-gif-16501897
    app.giantFast2 = scaleImage(app, app.loadImage('term project/images/fast2.png'), (180, 480))
    app.giantFast3 = scaleImage(app, app.loadImage('term project/images/fast3.png'), (180, 480))
    app.giantFast4 = scaleImage(app, app.loadImage('term project/images/fast4.png'), (180, 480))
    app.giantFastSprites = []
    app.giantFastSprites.extend([app.giantFast1, app.giantFast2, app.giantFast3, app.giantFast4])
    app.giantFastReversed1 = app.giantFast1.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    app.giantFastReversed2 = app.giantFast2.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    app.giantFastReversed3 = app.giantFast3.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    app.giantFastReversed4 = app.giantFast4.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    app.reversedGiantFast = []
    app.reversedGiantFast.extend([app.giantFastReversed1, app.giantFastReversed2, app.giantFastReversed3, app.giantFastReversed4])
    app.reverse = False
    app.spriteCounter = 0
    app.spriteDelay = 0
    addTerrain(app)
    addPowerUps(app)
    createFloor(app)
    createPlatform(app)
    createVines(app)
    createEnemies(app)
    app.powerUps.extend(placePowerUps(app.powerUpTypes, app.terrain))
    app.mudPatches.extend(placeMudPatches(app.terrain))

# advanced Tkinter mini-lecture https://scs.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=f19a16b4-d382-4021-b9e7-af43003eb620
def scaleImage(app, image, dimensions):
    ogWidth, ogHeight = image.size
    ogRatio = ogWidth/ogHeight
    width, height = dimensions
    goalRatio = width/height
    if ogRatio > goalRatio:
        scale = width/ogWidth
    else:
        scale = height/ogHeight
    return app.scaleImage(image, scale)
# ibid
def drawImage(app, canvas, image, cx, cy):
    canvas.create_image(cx, cy, image=ImageTk.PhotoImage(image))

# add terrain manually here
def addTerrain(app):
    # tkinter color list: http://cs111.wellesley.edu/archive/cs111_fall14/public_html/labs/lab12/tkintercolor.html 
    testLedge = Terrain(400, 30, [550, 250], 'sandy brown')
    app.terrain.append(testLedge)
    wall = Terrain(100, 300, [800, app.height-150], 'sandy brown')
    app.terrain.append(wall)
    pole = Terrain(50, 100, [app.mapSize-100, app.height-150], 'black')
    app.terrain.append(pole)
    vine = Terrain(10, app.height*1.5, [200, -125], 'chartreuse')
    app.vines.append(vine)
    mud = Terrain(200, 10, [120, app.height-30], 'OrangeRed4')
    app.mudPatches.append(mud)

#add power ups manually here
def addPowerUps(app):
    test1 = PowerUps(32, 32, [800, app.height-320], 'blue')
    test2 = PowerUps(32, 32, [100, app.height-60], 'purple')
    test3 = PowerUps(32, 32, [180, app.height-60], 'yellow')
    test4 = PowerUps(32, 32, [500, app.height-60], 'orange')
    app.powerUps.append(test1)
    app.powerUps.append(test2)
    app.powerUps.append(test3)
    app.powerUps.append(test4)

def createFloor(app):
    leftEdge = -200
    for hole in app.holes:
        length = (hole - 100 - leftEdge)
        midpoint = statistics.mean([leftEdge, hole-100])
        floor = Terrain(length, 100, [midpoint, app.height+20], 'green')
        app.terrain.append(floor)
        leftEdge = (hole + 100)
    length = (app.mapSize + 500 - leftEdge) #final stretch of floor
    midpoint = statistics.mean([app.mapSize+500, leftEdge])
    finalStretch = Terrain(length, 100, [midpoint, app.height+20], 'green')
    app.terrain.append(finalStretch)

def createPlatform(app):
    for platform in app.platformLocations:
        length = random.randint(200,300)
        height = random.randint(15, 30)
        ledge = Terrain(length, height, platform, 'sandy brown')
        app.platforms.append(ledge)
        app.terrain.append(ledge)

def createVines(app):
    locations = set()
    for i in range(4):
        locations.add(app.holes[random.randint(3, len(app.holes)-1)])
    for x in locations:
        vine = Terrain(10, app.height*2, [x-random.randint(30, 100), -180], 'chartreuse')
        app.vines.append(vine)

def createEnemies(app):
    for platform in app.platforms:
        adjusted = copy.copy(platform.position)
        adjusted[1] -= 50
        enemy = Character(35, random.randint(35, 50), adjusted)
        enemy.speedx = random.randint(3, 5)
        (left, top, right, bottom) = platform.getEdges()
        enemy.leftBound, enemy.rightBound = left, right
        app.enemies += [enemy]

def drawTerrain(app, canvas):
    for element in app.terrain:
        (x1, y1, x2, y2) = element.getEdges()
        canvas.create_rectangle(x1 - app.scrollX, y1 - app.scrollY, 
                                x2 - app.scrollX, y2 - app.scrollY, fill=element.color)
    for element in app.vines:
        (x1, y1, x2, y2) = element.getEdges()
        canvas.create_rectangle(x1 - app.scrollX, y1 - app.scrollY, 
                                x2 - app.scrollX, y2 - app.scrollY, fill=element.color)
    
    for element in app.mudPatches:
        (x1, y1, x2, y2) = element.getEdges()
        canvas.create_rectangle(x1 - app.scrollX, y1 - app.scrollY, 
                                x2 - app.scrollX, y2 - app.scrollY, fill=element.color)        

def drawEnemies(app, canvas):
    for enemy in app.enemies:
        (x1, y1, x2, y2) = enemy.getEdges()
        canvas.create_rectangle(x1 - app.scrollX, y1 - app.scrollY, 
                                x2 - app.scrollX, y2 - app.scrollY, fill='red')

def drawPowerUps(app, canvas):
    for powerUp in app.powerUps:
        (x1, y1, x2, y2) = powerUp.getEdges()
        canvas.create_oval(x1 - app.scrollX, y1 - app.scrollY, 
                                x2 - app.scrollX, y2 - app.scrollY, fill=powerUp.color)
    for projectile in app.projectiles:
        (x1, y1, x2, y2) = projectile.getEdges()
        canvas.create_rectangle(x1 - app.scrollX, y1 - app.scrollY, 
                                x2 - app.scrollX, y2 - app.scrollY, fill='DarkRed')      

#https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#sidescrollerExamples 
def sideScroll(app):
    if app.scrollX <= app.mapSize + 500:
        if (app.hero.position[0] < app.scrollX + app.scrollMargin):
            app.scrollX = app.hero.position[0] - app.scrollMargin
        if (app.hero.position[0] > app.scrollX + app.width - app.scrollMargin):
            app.scrollX = app.hero.position[0] - app.width + app.scrollMargin

def scroll(app):
    if app.hero.position[1] <= app.height:
        if (app.hero.position[1] < app.scrollY + app.scrollMarginY):
            app.scrollY = app.hero.position[1] - app.scrollMarginY
        if (app.hero.position[1] > app.scrollY + app.height - app.scrollMarginY):
            app.scrollY = app.hero.position[1] - app.height + app.scrollMarginY

def keyPressed(app, event):
    if event.key == 'r':
        appStarted(app)
    if app.startGame or app.tutorial:
        if event.key == 't':
            app.startGame = False
        if event.key == 'p':
            app.tutorial = not app.tutorial
            app.startGame = not app.startGame

    else:
        if app.onVine:
            if event.key == 'Up':
                app.hero.position[1] -= 2
            elif event.key == 'Down':
                app.hero.position[1] += 2
            if (event.key == 'Left') or (event.key == 'Right'):
                app.onVine = False
        if abs(app.hero.speedx) < app.maxSpeed:
            if event.key == 'Left':
                app.hero.speedx -= 2.5
                app.reverse = True
            if event.key == 'Right':
                app.hero.speedx += 2.5
                app.reverse = False
        if app.hero.air == False:
            if event.key == "Up":
                if app.onMud:
                    app.hero.speedy += 6
                    app.onMud = False
                else:
                    app.hero.speedy += 12
                app.hero.air = True
        if event.key == 'e' and len(app.items) > 0:
            app.items[0].toss(app.reverse)
            app.items.pop(0)
        if app.ammo > 0:
            if event.key == 'f':
                app.ammo -= 1
                projectile = Character(30, 5, copy.copy(app.hero.position))
                if app.reverse:
                    projectile.position[0] -= app.hero.width/2
                else:
                    projectile.position[0] += app.hero.width/1.5
                app.projectiles.append(projectile)
                projectile.shoot(app.reverse)
        #for testing only (losing health on purpose)
        if event.key == 'q':
            app.lives -= 1
            app.damageTaken = True

def keyReleased(app, event):
    if (event.key == 'Left') or (event.key == 'Right'):
        app.hero.speedx = 0

def timerFired(app): 
    if not (app.startGame or app.tutorial):
        if (app.lives <= 0) or (app.timePassed//40 > app.timeLimit):
            app.gameOver = True
            return
        elif app.damageTaken:
            app.deathTimer += 1
            if app.deathTimer >= 100:
                app.damageTaken = False
                if app.giant:
                    app.giant = False
                    app.hero.width /= 1.5
                    app.hero.height /= 1.5
                if app.fast:
                    app.fast = False
                    app.maxSpeed = 4
                for powerUp in app.powerUps:
                    if powerUp.held:
                        app.powerUps.remove(powerUp)
                app.deathTimer = 0
                app.scrollY = 0
                app.scrollX = 0
                app.hero.position = [150, 0.7*app.height]
            return
        elif app.hero.position[0] >= (app.mapSize - 200):
            app.victory = True
            return

        for enemy in app.enemies:
            enemy.boundary()
            enemy.move()
        for powerUp in app.powerUps:
            if powerUp.picked(app.hero):
                if powerUp.color == 'purple':
                    if not powerUp.held:
                        powerUp.held = True
                        app.items.append(powerUp)
                elif powerUp.color == 'orange':
                    app.ammo += 5
                    app.powerUps.remove(powerUp)
                else:
                    app.powerUps.remove(powerUp)
                    if powerUp.color == 'blue' and not app.giant:    
                        app.giant = True
                        app.hero.width *= 1.5
                        app.hero.height *= 1.3
                    elif powerUp.color == 'yellow':    
                        app.fast = True
                        app.maxSpeed = 7
            if powerUp.tossed:
                powerUp.speedy += app.gravity
                powerUp.move()
                powerUp.jump()
                if powerUp.collidey(app.terrain):
                    app.hero.position = powerUp.position
                    app.powerUps.remove(powerUp)
            elif powerUp.held:
                powerUp.position[0] = app.hero.position[0]
                powerUp.position[1] = app.hero.position[1] - app.hero.height

        (left, top, right, bottom) = app.hero.getEdges()
        if left <= 0:
            app.hero.position[0] += 0.1
        else:
            app.hero.move()
            sideScroll(app)
        if app.onVine:
            app.spriteCounter = 0
        elif app.hero.air:
            app.spriteCounter = 1
        elif app.hero.speedx == 0:
            app.spriteCounter = 3
        else:
            app.spriteDelay += 1
            app.spriteCounter = app.spriteDelay//4 % len(app.sprites)
        
        for element in app.terrain:
            if element.collidex(app.hero):
                app.hero.speedx -= 2*app.hero.speedx
                app.hero.speedy = 0
                app.hero.air = True
        for vine in app.vines:
            if vine.collidex(app.hero) and app.hero.air:
                app.hero.speedx = 0
                app.onVine = True
        for enemy in app.enemies:
            if ((abs(app.hero.position[0] - enemy.position[0]) < 300) and 
            (abs(app.hero.position[1] - enemy.position[1]) < 100)):
                if app.timePassed % random.randint(40, 55) == 0:
                    enemy.speedy += 6
            if enemy.collidex(app.hero):
                if not app.giant:
                    app.lives -= 1
                    app.damageTaken = True
                else:
                    app.enemies.remove(enemy)
                    app.giant = False
                    app.hero.height /= 1.3
                    app.hero.width /= 1.5
                return
            # allows the player to kill an enemy by stomping on them
            # elif enemy.collidey([app.hero]):
            #     app.enemies.remove(enemy)
            #     app.hero.speedy += 15   
            #     app.hero.air = True
            #     app.hero.jump()
        for projectile in app.projectiles:
            projectile.move()
            for enemy in app.enemies:
                if projectile.collidex(enemy):
                    app.enemies.remove(enemy)
                    app.projectiles.remove(projectile)
        scroll(app)
        if app.onVine:
            app.gravity = 0
            app.air = False
            app.hero.speedy = 0
        else:
            app.gravity = -0.5
        app.hero.jump()
        if not app.hero.collidey(app.terrain):
            app.hero.speedy += app.gravity
        if app.hero.collidey(app.mudPatches):
            app.onMud = True
        for enemy in app.enemies:
            enemy.jump()
            if not enemy.collidey(app.terrain):
                enemy.speedy += app.gravity
        if app.hero.position[1] > 1.5*app.height:
            app.lives -= 1
            app.damageTaken = True
            return
        app.timePassed += 1

def gameStartScreen(app, canvas):
    canvas.create_text(app.width/2, app.height/2-30, text="PUSHEEN'S 15-112 ADVENTURE!!", font='Impact 36', fill='black')
    canvas.create_text(app.width/2, app.height/2+30, text="Press 't' to start game", font='Impact 18', fill='black')
    canvas.create_text(app.width/2, app.height/2+60, text="Press 'p' for instructions", font='Impact 18', fill='black')

def tutorialScreen(app, canvas):
    canvas.create_text(app.width/2, 30, text="Use Arrow Keys to Move", font='Impact 18', fill='black')
    canvas.create_text(app.width/2, 70, text="Vines let you climb up and down them", font='Impact 18', fill='black')
    canvas.create_text(app.width/2, 110, text="Mud patches make it harder to jump", font='Impact 18', fill='black')
    canvas.create_text(app.width/2, 160, text="Beat the game by reaching the end of the map!", font='Impact 20', fill='black')
    canvas.create_text(app.width/2, app.height/2, text="AVOID THE RED ENEMIES!!", font='Impact 28', fill='black')
    canvas.create_text(app.width/8, 260, text="Power Ups:", font='Impact 18', fill='black')
    canvas.create_oval(app.width/8-10, 290-10, app.width/8+10, 290+10, fill='blue')
    canvas.create_oval(app.width/8-10, 320-10, app.width/8+10, 320+10, fill='yellow')
    canvas.create_oval(app.width/8-10, 350-10, app.width/8+10, 350+10, fill='purple')
    canvas.create_oval(app.width/8-10, 380-10, app.width/8+10, 380+10, fill='orange')
    canvas.create_text(app.width/8+50, 290, text="Size-Up", font='Impact 12', fill='black')
    canvas.create_text(app.width/8+65, 320, text="Speed Boost", font='Impact 12', fill='black')
    canvas.create_text(app.width/8+114, 350, text="Teleport [press 'e' to throw]", font='Impact 12', fill='black')
    canvas.create_text(app.width/8+101, 380, text="SHOOT! [press 'f' to fire]", font='Impact 12', fill='black')
    canvas.create_text(app.width*0.8, app.height-25, text="Press 'p' to exit tutorial screen", font='Impact 18', fill='black')

#https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#imageMethods
def drawBackground(app, canvas):
    width, height = app.dimensions
    # canvas.create_image(0, 300, image=ImageTk.PhotoImage(app.background))
    drawImage(app, canvas, app.background, app.width/2, height/2)

def youDiedScreen(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill='black')
    if app.lives > 1:
        canvas.create_text(app.width/2, app.height/2, text=f'You Died! \nx{app.lives} lives left', 
                           font='Impact 32', fill='white')
    else:  
        canvas.create_text(app.width/2, app.height/2, text=f'You Died \nx{app.lives} life left', 
                           font='Impact 32', fill='white')

def gameOverScreen(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill='black')
    if app.lives > 0:
        canvas.create_text(app.width/2, app.height/2-50, text='Out of time!', font='Impact 30', fill='white')
    canvas.create_text(app.width/2, app.height/2, text='Game Over', font='Impact 36', fill='white')
    canvas.create_text(app.width/2, app.height/2+60, text="Press 'R' to restart", font='Impact 18', fill='white')

def victoryScreen(app, canvas):
    canvas.create_text(app.width/2, app.height/2, text='VICTORY!!!', font='Impact 36', fill='black')

def redrawAll(app, canvas):
    if app.startGame:
        gameStartScreen(app, canvas)
    elif app.tutorial:
        tutorialScreen(app, canvas)
    elif app.gameOver:
        gameOverScreen(app, canvas)
    elif app.damageTaken:
        youDiedScreen(app, canvas)
    elif app.victory:
        victoryScreen(app, canvas)
    else:
        drawBackground(app, canvas)
        sx = app.scrollX
        sy = app.scrollY
        if app.giant and app.fast:
            if app.reverse: 
                sprite = app.reversedGiantFast[app.spriteCounter]
            else:
                sprite = app.giantFastSprites[app.spriteCounter]
        elif app.giant and app.reverse:
            sprite = app.reversedGiantSprites[app.spriteCounter]
        elif app.fast and app.reverse:
            sprite = app.reversedFastSprites[app.spriteCounter]
        elif app.giant:
            sprite = app.giantSprites[app.spriteCounter]
        elif app.fast:
            sprite = app.fastSprites[app.spriteCounter]
        elif app.reverse:
            sprite = app.reversedSprites[app.spriteCounter]
        else:
            sprite = app.sprites[app.spriteCounter]
        (left, top, right, bottom) = app.hero.getEdges()
        canvas.create_rectangle(left - sx, top - sy, right - sx, bottom - sy, outline='skyblue')
        canvas.create_image(app.hero.position[0] - sx, app.hero.position[1] - sy, 
                            image=ImageTk.PhotoImage(sprite))
        drawTerrain(app, canvas)
        drawPowerUps(app, canvas)
        drawEnemies(app, canvas)
        canvas.create_text(-130 - sx, app.height/3, text='edge of the map bro', font='Impact 16', fill='black')
        canvas.create_text(650, 25, 
                           text=f'Ammo: {app.ammo}\tTime {app.timePassed//40}\tLives x{app.lives}', 
                           font='Helvetica 16')


runApp(width=800, height=400)