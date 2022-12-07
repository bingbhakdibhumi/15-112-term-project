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
    app.vines = []
    app.onVine = False
    app.enemies = []
    app.powerUps = []
    app.items = []
    app.numberOfHoles = 8
    app.holes = createHoles(1000, app.mapSize-300, app.numberOfHoles, 500) #start, stop, amount, margin
    app.numberOfPlatforms = 20
    app.platformLocations = createPlatforms(1200, app.mapSize-300, app.numberOfPlatforms, 
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
    testLedge = Terrain(400, 30, [550, 250], 'brown')
    app.terrain.append(testLedge)
    wall = Terrain(100, 300, [800, app.height-150], 'brown')
    app.terrain.append(wall)
    pole = Terrain(40, 300, [app.mapSize-200, app.height-150], 'brown')
    app.terrain.append(pole)
    vine = Terrain(10, app.height*2, [200, -125], 'chartreuse')
    app.vines.append(vine)

#add power ups manually here
def addPowerUps(app):
    test1 = PowerUps(30, 30, [800, app.height-320], 'blue')
    test2 = PowerUps(30, 30, [1000, app.height-60], 'yellow')
    test3 = PowerUps(32, 32, [200, app.height-60], 'black')
    app.powerUps.append(test1)
    app.powerUps.append(test2)
    app.powerUps.append(test3)

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
        length = random.randint(270,350)
        height = random.randint(15, 35)
        ledge = Terrain(length, height, platform, 'brown')
        app.platforms.append(ledge)
        app.terrain.append(ledge)

def createVines(app):
    locations = []
    for i in range(10):
        locations.append(app.holes[random.randint(0, len(app.holes)-1)])
    for x in locations:
        vine = Terrain(10, app.height*2, [x, -150], 'chartreuse')
        app.vines.append(vine)

def createEnemies(app):
    for platform in app.platforms:
        adjusted = copy.copy(platform.position)
        adjusted[1] -= 50
        enemy = Character(35, 35, adjusted)
        enemy.speedx = random.randint(2, 4)
        enemy.speedy = 5
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
def drawEnemies(app, canvas):
    for enemy in app.enemies:
        (x1, y1, x2, y2) = enemy.getEdges()
        canvas.create_oval(x1 - app.scrollX, y1 - app.scrollY, 
                                x2 - app.scrollX, y2 - app.scrollY, fill='red')

def drawPowerUps(app, canvas):
    for powerUp in app.powerUps:
        (x1, y1, x2, y2) = powerUp.getEdges()
        canvas.create_oval(x1 - app.scrollX, y1 - app.scrollY, 
                                x2 - app.scrollX, y2 - app.scrollY, fill=powerUp.color)       

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
    if app.startGame:
        if event.key == 't':
            app.startGame = False
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
                app.hero.speedy += 12
                app.hero.air = True
        if len(app.items) > 0:
            if event.key == 'f':
                app.items[0].toss(app.reverse)

        if event.key == 'q':
            app.lives -= 1
            app.damageTaken = True

def keyReleased(app, event):
    if (event.key == 'Left') or (event.key == 'Right'):
        app.hero.speedx = 0

def timerFired(app): 
    if not app.startGame:
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
        elif app.hero.position[0] >= (app.mapSize - 250):
            app.victory = True
            return

        for enemy in app.enemies:
            enemy.boundary()
            enemy.move()
        for powerUp in app.powerUps:
            if powerUp.picked(app.hero):
                if powerUp.color == 'black':
                    powerUp.held = True
                    app.items.append(powerUp)
                else:
                    app.powerUps.remove(powerUp)
                    if powerUp.color == 'blue':    
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
            if ((abs(app.hero.position[0] - enemy.position[0]) < 400) and 
            (abs(app.hero.position[1] - enemy.position[1]) < 50)):
                if app.timePassed % 45 == 0:
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
            elif enemy.collidey([app.hero]):
                app.enemies.remove(enemy)
                app.hero.speedy += 15   
                app.hero.air = True
                app.hero.jump()
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
    pass

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
        canvas.create_text(650, 25, text=f'Time {app.timePassed//40}\tLives x{app.lives}', font='Helvetica 16')


runApp(width=800, height=400)