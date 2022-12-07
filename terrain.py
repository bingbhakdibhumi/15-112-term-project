from gameObjects import *
import random
import copy

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

def placePowerUps(powerUps, terrain):
    result = []
    repeats = set()
    for element in powerUps:
        count = 0
        while count < powerUps[element]:
            index = random.randint(4, len(terrain)-1)
            if index not in repeats:
                repeats.add(index)
                location = terrain[index]
                coordinates = copy.copy(location.position)
                coordinates[0] += location.width/3
                if location.height > 70:
                    coordinates[1] -= 70
                else:
                    coordinates[1] -= 1.5*location.height
                result.append(PowerUps(32, 32, coordinates, element))
                count += 1
    return result

def placeMudPatches(terrain):
    result = []
    repeats = set()
    count = 0
    while count < 10:
        index = random.randint(3, len(terrain)-1)
        if index not in repeats:
            repeats.add(index)
            location = terrain[index]
            (left, top, right, bottom) = location.getEdges()
            coordinates = copy.copy(location.position)
            coordinates[0] += random.randint(-50, 50)
            coordinates[1] = top
            result.append(Terrain(random.randint(125, 200), 10, coordinates, 'OrangeRed4'))
            count += 1
    return result