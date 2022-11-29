from cmu_112_graphics import *
from gameObjects import *
import random
import time
import math
import copy

def appStarted(app):
    app.dimensions = (900, 400)
    app.mapSize = 6400
    app.scrollX = 0 
    app.scrollY = 0
    app.scrollMargin = 150
    app.scrollMarginY = 50
    app.spawny = app.height/2
    app.spawnx = app.width/2
    app.timerDelay = 5
    app.gravity = -0.5
    app.terrain = []
    app.terrainxy = []
    app.enemies = []
    app.hero = hero(55, 40, [app.scrollMargin, 0.7*app.height])
    addTerrain(app)
    app.lives = 3
    app.timePassed = 0
    app.timeLimit = 200
    app.deathTimer = 0
    app.damageTaken = False
    app.gameOver = False
    app.victory = False
    app.background = scaleImage(app, app.loadImage('term project/images/background.jpg'), app.dimensions) #https://www.freepik.com/premium-vector/pixel-art-sky-background-with-clouds-cloudy-blue-sky-vector-8bit-game-white-background_26733992.htm
    app.sprite1 = scaleImage(app, app.loadImage('term project/images/pusheen1.png'), (120, 320)) #https://tenor.com/view/pusheen-running-cat-cute-chase-gif-16501897
    app.sprite2 = scaleImage(app, app.loadImage('term project/images/pusheen2.png'), (120, 320))
    app.sprite3 = scaleImage(app, app.loadImage('term project/images/pusheen3.png'), (120, 320))
    app.sprite4 = scaleImage(app, app.loadImage('term project/images/pusheen4.png'), (120, 320))
    # https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#spritesheetsWithCropping
    app.sprites = []
    app.sprites.extend([app.sprite1, app.sprite2, app.sprite3, app.sprite4])
    app.reversed1 = app.sprite1.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    app.reversed2 = app.sprite2.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    app.reversed3 = app.sprite3.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    app.reversed4 = app.sprite4.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    app.reversedSprites = []
    app.reversedSprites.extend([app.reversed1, app.reversed2, app.reversed3, app.reversed4])
    app.reverse = False
    app.spriteCounter = 0
    app.spriteDelay = 0

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

# new terrain can be added here
def addTerrain(app):
    testLedge = terrain(400, 30, [500, 230])
    app.terrain.append(testLedge)
    floor = terrain(9000, 30, [4000, app.height-15])
    app.terrain.append(floor)
    wall = terrain(100, 300, [800, app.height-150])
    app.terrain.append(wall)
    pole = terrain(40, 300, [6200, app.height-150])
    app.terrain.append(pole)

# def createTerrain(app):
#     for element in app.terrainxy:
#         app.terrain.append(terrain(height, width, [position]))

def drawTerrain(app, canvas):
    for element in app.terrain:
        (x1, y1, x2, y2) = element.getEdges()
        canvas.create_rectangle(x1 - app.scrollX, y1 - app.scrollY, 
                                x2 - app.scrollX, y2 - app.scrollY, fill='green')

#https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#sidescrollerExamples 
def sideScroll(app):
    if app.scrollX <= app.mapSize:
        if (app.hero.position[0] < app.scrollX + app.scrollMargin):
            app.scrollX = app.hero.position[0] - app.scrollMargin
        if (app.hero.position[0] > app.scrollX + app.width - app.scrollMargin):
            app.scrollX = app.hero.position[0] - app.width + app.scrollMargin

def scroll(app):
    if (app.hero.position[1] < app.scrollY + app.scrollMarginY):
        app.scrollY = app.hero.position[1] - app.scrollMarginY
    if (app.hero.position[1] > app.scrollY + app.height - app.scrollMarginY):
        app.scrollY = app.hero.position[1] - app.height + app.scrollMarginY

def keyPressed(app, event):
    if event.key == 'r':
        appStarted(app)
    if abs(app.hero.speedx) < 4:
        if event.key == 'Left':
            app.hero.speedx -= 2.5
            app.reverse = True
        if event.key == 'Right':
            app.hero.speedx += 2.5
            app.reverse = False
    if app.hero.air == False:
        if event.key == "Up":
            app.hero.speedy += 13
            app.hero.air = True
    if event.key == 'q':
        app.lives -= 1
        app.damageTaken = True

def keyReleased(app, event):
    if (event.key == 'Left') or (event.key == 'Right'):
        app.hero.speedx = 0


def timerFired(app): 
    if (app.lives <= 0) or (app.timePassed//20 > app.timeLimit):
        app.gameOver = True
        return
    elif app.damageTaken:
        app.deathTimer += 1
        if app.deathTimer >= 100:
            app.damageTaken = False
            app.deathTimer = 0
            app.hero.position = [150, 0.7*app.height]
        return
    elif app.hero.position[0] >= 6150:
        app.victory = True
        return
    (left, top, right, bottom) = app.hero.getEdges()

    if left <= 0:
        app.hero.position[0] += 0.1
    else:
        app.hero.move()
        sideScroll(app)

    if app.hero.air:
        app.spriteCounter = 1
    elif app.hero.speedx == 0:
        app.spriteCounter = 3
    else:
        app.spriteDelay += 1
        app.spriteCounter = app.spriteDelay//5 % len(app.sprites)
    
    for element in app.terrain:
        if element.collidex(app.hero):
            app.hero.speedx -= 2*app.hero.speedx
            app.hero.air = True
    scroll(app)
    app.hero.jump()
    if not app.hero.collidey(app.terrain):
        app.hero.speedy += app.gravity
    if app.hero.position[1] > 1.5*app.height:
        app.gameOver = True
    
    app.timePassed += 1

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
        canvas.create_text(app.width/2, app.height/2, text=f'You Died! \nx{app.lives} life left', 
                           font='Impact 32', fill='white')

def gameOverScreen(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill='black')
    if app.lives > 0:
        canvas.create_text(app.width/2, app.height/2-50, text='Out of time!', font='Impact 30', fill='white')
    canvas.create_text(app.width/2, app.height/2, text='Game Over', font='Impact 36', fill='white')
    canvas.create_text(app.width/2, app.height/2+60, text="Press 'r' to restart", font='Impact 18', fill='white')

def victoryScreen(app, canvas):
    canvas.create_text(app.width/2, app.height/2, text='VICTORY!!!', font='Impact 36', fill='black')

def redrawAll(app, canvas):
    if app.gameOver:
        gameOverScreen(app, canvas)
    elif app.damageTaken:
        youDiedScreen(app, canvas)
    elif app.victory:
        victoryScreen(app, canvas)
    else:
        drawBackground(app, canvas)
        sx = app.scrollX
        sy = app.scrollY
        if app.reverse:
            sprite = app.reversedSprites[app.spriteCounter]
        else:
            sprite = app.sprites[app.spriteCounter]
        (left, top, right, bottom) = app.hero.getEdges()
        canvas.create_rectangle(left - sx, top - sy, right - sx, bottom - sy)
        canvas.create_image(app.hero.position[0] - sx, app.hero.position[1] - sy, 
                            image=ImageTk.PhotoImage(sprite))
        drawTerrain(app, canvas)
        canvas.create_text(650, 25, text=f'Time {app.timePassed//40}\tLives x{app.lives}', font='Helvetica 16')
        
    

runApp(width=800, height=400)