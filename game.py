from cmu_112_graphics import *
from gameObjects import *
import random
import time
import math

def appStarted(app):
    app.dimensions = (900, 400)
    app.mapSize = 6400
    app.scrollX = 0 
    app.scrollMargin = 150
    app.spawny = app.height/2
    app.spawnx = app.width/2
    app.timerDelay = 5
    app.gravity = -0.5
    app.terrain = []
    app.terrainxy = []
    app.enemies = []
    app.hero = hero(40, 45, [app.scrollMargin, app.height/2])
    app.heroSize = (120, 320)
    addTerrain(app)
    app.gameOver = False
    app.background = scaleImage(app, app.loadImage('term project/images/background.jpg'), app.dimensions) #https://www.freepik.com/premium-vector/pixel-art-sky-background-with-clouds-cloudy-blue-sky-vector-8bit-game-white-background_26733992.htm
    app.sprite1 = scaleImage(app, app.loadImage('term project/images/pusheen1.png'), app.heroSize) #https://tenor.com/view/pusheen-running-cat-cute-chase-gif-16501897
    app.sprite2 = scaleImage(app, app.loadImage('term project/images/pusheen2.png'), app.heroSize)
    app.sprite3 = scaleImage(app, app.loadImage('term project/images/pusheen3.png'), app.heroSize)
    app.sprite4 = scaleImage(app, app.loadImage('term project/images/pusheen4.png'), app.heroSize)
    # https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#spritesheetsWithCropping
    app.sprites = []
    app.sprites.extend([app.sprite1, app.sprite2, app.sprite3, app.sprite4])
    app.spriteCounter = 0

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
    testLedge = terrain(30, 400, [500, 230])
    app.terrain.append(testLedge)
    floor = terrain(20, 9000, [4000, app.height-15])
    app.terrain.append(floor)
    # wall = terrain(300, 30, [800, app.height-150])
    # app.terrain.append(wall)

# def createTerrain(app):
#     for element in app.terrainxy:
#         app.terrain.append(terrain(height, width, [position]))

def drawTerrain(app, canvas):
    for element in app.terrain:
        (x1, y1, x2, y2) = element.getEdges()
        canvas.create_rectangle(x1 - app.scrollX, y1, x2 - app.scrollX, y2, fill='green')

#https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#sidescrollerExamples 
def sideScroll(app):
    if app.scrollX <= app.mapSize:
        if (app.hero.position[0] < app.scrollX + app.scrollMargin):
            app.scrollX = app.hero.position[0] - app.scrollMargin
        if (app.hero.position[0] > app.scrollX + app.width - app.scrollMargin):
            app.scrollX = app.hero.position[0] - app.width + app.scrollMargin

def keyPressed(app, event):
    if abs(app.hero.speedx) < 4:
        if event.key == 'Left':
            app.spriteCounter = (1 + app.spriteCounter) % len(app.sprites)
            app.hero.speedx -= 2.5
        if event.key == 'Right':
            app.spriteCounter = (1 + app.spriteCounter) % len(app.sprites)
            app.hero.speedx += 2.5
    if app.hero.air == False:
        if event.key == "Up":
            app.hero.speedy += 13
            app.hero.air = True
    if event.key == 'r':
        appStarted(app)

def keyReleased(app, event):
    if (event.key == 'Left') or (event.key == 'Right'):
        app.hero.speedx = 0

def sizeChanged(app):
    sideScroll(app)

def timerFired(app): 
    if app.scrollX >= 6400:
        app.gameOver = True

    (left, top, right, bottom) = app.hero.getEdges()

    if left <= 0:
        app.hero.position[0] += 0.1
    else:
        # app.spriteCounter = (1 + app.spriteCounter) % len(app.sprites)
        app.hero.move()
        sideScroll(app)
    if app.hero.air:
        app.spriteCounter = 1
    elif app.hero.speedx > 0:
        app.spriteCounter = (1 + app.spriteCounter) % len(app.sprites)
    elif app.hero.speedx < 0:
        pass
    for element in app.terrain:
        if element.collidex(app.hero):
            app.hero.speedx -= 2*app.hero.speedx
            app.hero.air = True

    app.hero.jump()
    if not app.hero.collidey(app.terrain):
        app.hero.speedy += app.gravity

#https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#imageMethods
def drawBackground(app, canvas):
    width, height = app.dimensions
    # canvas.create_image(0, 300, image=ImageTk.PhotoImage(app.background))
    drawImage(app, canvas, app.background, app.width/2, height/2)

def gameOverScreen(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill='black')
    canvas.create_text(app.width/2, app.height/2, text='Game Over', font='Impact 36', fill='white')

def victoryScreen(app, canvas):
    pass

def redrawAll(app, canvas):
    if app.gameOver:
        gameOverScreen(app, canvas)
    else:
        drawBackground(app, canvas)
        sx = app.scrollX
        sprite = app.sprites[app.spriteCounter]
        (left, top, right, bottom) = app.hero.getEdges()
        canvas.create_rectangle(left - sx, top, right - sx, bottom,
                                fill = 'brown')
        canvas.create_image(app.hero.position[0] - sx, app.hero.position[1], image=ImageTk.PhotoImage(sprite))
        drawTerrain(app, canvas)
    

runApp(width=800, height=400)