from cmu_112_graphics import *
from gameObjects import *
import random
import time

def appStarted(app):
    app.scrollX = 0 
    app.scrollMargin = 50
    app.spawny = app.height/2
    app.spawnx = app.width/2
    app.timerDelay = 5
    app.gravity = -0.5
    app.terrain = []
    app.enemies = []
    app.hero = hero(50, 30, [app.scrollMargin, app.height/2])
    addTerrain(app)
    app.gameOver = False

#new terrain can be added here
def addTerrain(app):
    testLedge = terrain(30, 400, [500, 100])
    app.terrain.append(testLedge)
    floor = terrain(30, app.width, [app.width/2, app.height-15])
    app.terrain.append(floor)

def drawTerrain(app, canvas):
    for element in app.terrain:
        (x1, y1, x2, y2) = element.getEdges()
        canvas.create_rectangle(x1 - app.scrollX, y1, x2 - app.scrollX, y2, fill='green')

#https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#sidescrollerExamples 
def sideScroll(app):
    if (app.hero.position[0] < app.scrollX + app.scrollMargin):
        app.scrollX = app.hero.position[0] - app.scrollMargin
    if (app.hero.position[0] > app.scrollX + app.width - app.scrollMargin):
        app.scrollX = app.hero.position[0] - app.width + app.scrollMargin

# def checkCollision(app, x, y, height, width):
#     for element in app.terrain:
#         (x1, y1, x2, y2) = element.getEdges()
#         if ((x + width/2 > x1) and (x - width/2 < x2) and
#             (y + height/2 > y1) and (y - height/2 < y1)):
#             return False
#     return True


def keyPressed(app, event):
    if abs(app.hero.speedx) < 3:
        if event.key == 'Left':
            app.hero.speedx -= 1.5
        if event.key == 'Right':
            app.hero.speedx += 1.5
    if app.hero.air == False:
        if event.key == "Up":
            app.hero.speedy += 15
            app.hero.air = True

def keyReleased(app, event):
    if (event.key == 'Left') or (event.key == 'Right'):
        app.hero.speedx = 0

def sizeChanged(app):
    sideScroll(app)

def timerFired(app): 
    if app.scrollX >= 2000:
        app.gameOver = True
        
    app.hero.move()
    sideScroll(app)
    app.hero.jump()

    (left, top, right, bottom) = app.hero.getEdges()

    if not app.hero.collidey(app.terrain):
        app.hero.speedy += app.gravity

def gameOverScreen(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill='black')
    canvas.create_text(app.width/2, app.height/2, text='Game Over', font='Impact 36', fill='white')

def victoryScreen(app, canvas):
    pass

def redrawAll(app, canvas):
    if app.gameOver:
        gameOverScreen(app, canvas)
    else:
        sx = app.scrollX
        (left, top, right, bottom) = app.hero.getEdges()
        canvas.create_rectangle(left - sx, top, right - sx, bottom,
                                fill = 'brown')
        drawTerrain(app, canvas)
    

runApp(width=800, height=400)