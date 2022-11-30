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

def createPlatforms(start, stop, amount, low, high, jumpHeight):
    xPositions = []
    count = 0
    while count < amount:
        location = random.randint(start, stop)
        if notOverlapping(location, xPositions, 50):
            xPositions.append(location)
            count += 1
    xPositions = sorted(xPositions)
    result = getPlatformHeight(xPositions, low, high, jumpHeight)
    return result

def getPlatformHeight(locations, low, high, jumpHeight):
    result = []
    for i in range (len(locations)):
        if i == 0:
            result.append([locations[i], low])
            result.append([locations[i+1], low-jumpHeight])
        elif i == 1:
            continue
        else:
            index = (-1**random.randint(0, 1))
            previousY = result[-1][1]
            if ((previousY + (jumpHeight*index) < high) or 
                (previousY + (jumpHeight*index) > low)):
                index = -index
            result.append([locations[i], previousY + (jumpHeight*index)])
    return result

print(createPlatforms(0, 8000, 10, 230, -100, 140))
