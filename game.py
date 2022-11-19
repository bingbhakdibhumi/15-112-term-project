from cmu_112_graphics import *
import random
import time

def appStarted(app):
    app.spawny = app.height/2
    app.spawnx = app.width/2
    app.timerDelay = 10
    app.gravity = 1

def keyPressed(app, event):
    if event.key == 'w':
        app.spawny -= 10
    if event.key == 's':
        app.spawny += 10
    if event.key == 'a':
        app.spawnx -= 10
    if event.key == 'd':
        app.spawnx += 10

def timerFired(app):
    
    if app.spawny + 25 < app.height:
        app.spawny += app.gravity




def redrawAll(app, canvas):
    canvas.create_rectangle(app.spawnx-15, app.spawny-25, app.spawnx+15, app.spawny+25, fill='red')


runApp(width=400, height=400)