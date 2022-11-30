from gameObjects import *
import random

#inspiration from Riley Krzywda
def createHoles(start, stop, amount, margin): #minimum distance between each hole
    if (margin*amount) >= (stop-start): #By the Pigeonhole principle, there will be an overlapping of margins
        return False #thus we return False because we can't properly create the holes this way
    xPositions = []
    count = 0
    while count < amount:
        location = random.randint(start, stop)
        if notOverlapping(location, xPositions, margin):
            xPositions.append(location)
            count += 1
    return sorted(xPositions)

#helper function to make sure there's no overlapping
def notOverlapping(location, elements, margin):
    for x in elements:
        if (((location > x) and (location < x+margin)) or
        ((location < x) and (location > x-margin))): 
            return False
    return True

def createPlatforms(start, stop, amount, low, high, yRange):
    xPositions = []
    count = 0
    while count < amount:
        location = random.randint(start, stop)
        if notOverlapping(location, xPositions, 50):
            xPositions.append(location)
            count += 1
    xPositions = sorted(xPositions)
    result = getPlatformHeight(xPositions, low, high, yRange)
    return result

def getPlatformHeight(locations, low, high, yRange):
    result = []
    for i in range (len(locations)):
        if i%3 == 0:
            result.append([locations[i], low])
        elif i%3 == 1:
            result.append([locations[i], low-yRange])
        else:
            index = (-1**random.randint(0, 1))
            previousY = result[-1][1]
            if ((previousY + (yRange*index) < high) or 
                (previousY + (yRange*index) > low)):
                index = -index
            result.append([locations[i], previousY + (yRange*index)])
    return result
