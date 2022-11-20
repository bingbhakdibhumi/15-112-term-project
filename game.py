from cmu_112_graphics import *
import random
import time

def appStarted(app):
    app.spawny = app.height/2
    app.spawnx = app.width/2
    app.timerDelay = 5
    app.gravity = 1
    app.terrain = []
    app.enemies = []
    app.test = character(5, 50, 30, app.width/4, app.height/2)
    addTerrain(app)

class character:
    def __init__(self, speed, height, width, x, y):
        self.speed = speed
        self.height = height
        self.width = width
        self.x = x 
        self.y = y

    def moveLeft(self):
        self.x -= self.speed
    def moveRight(self):
        self.x += self.speed
    def moveUp(self):
            self.y -= self.speed*10
    def moveDown(self):
        if self.y + self.height/2 < 400:
            self.y += self.speed/2

class terrain:
    def __init__(self, height, width, x, y):
        self.height = height
        self.width = width
        self.x = x 
        self.y = y
    
    def getVertices(self):
        x1 = self.x - self.width/2
        y1 = self.y - self.height/2
        x2 = self.x + self.width/2
        y2 = self.y + self.height/2
        return (x1, y1, x2, y2)

#new terrain can be added here
def addTerrain(app):
    testLedge = terrain(30, 400, 500, 275)
    app.terrain.append(testLedge)
    floor = terrain (30, app.width, app.width/2, app.height-15)
    app.terrain.append(floor)

def drawTerrain(app, canvas):
    for element in app.terrain:
        canvas.create_rectangle(element.getVertices(), fill='green')

def checkCollision(app, x, y, height, width):
    for element in app.terrain:
        (x1, y1, x2, y2) = element.getVertices()
        if ((x + width/2 > x1) and (x - width/2 < x2) and
            (y + height/2 > y1) and (y - height/2 < y1)):
            return False
    return True

def keyPressed(app, event):
    if event.key == 'w':
        app.spawny -= 10
    if event.key == 's':
        app.spawny += 10
    if event.key == 'a':
        app.spawnx -= 5
    if event.key == 'd':
        app.spawnx += 5
    
    if event.key == 'Left':
        app.test.moveLeft()
    if event.key == 'Right':
        app.test.moveRight()
    if event.key == 'Up':
        app.test.moveUp()

def timerFired(app): 
    if app.spawny + 25 < app.height:
        app.spawny += app.gravity

    if checkCollision(app, app.test.x, app.test.y, app.test.height, app.test.width):    
        app.test.moveDown()

def redrawAll(app, canvas):
    canvas.create_rectangle(app.spawnx-15, app.spawny-25, 
                            app.spawnx+15, app.spawny+25, 
                            fill='red')
    canvas.create_rectangle(app.test.x-(app.test.width/2), app.test.y-(app.test.height/2),
                            app.test.x+(app.test.width/2), app.test.y+(app.test.height/2),
                            fill = 'brown')
    drawTerrain(app, canvas)
    

runApp(width=800, height=400)