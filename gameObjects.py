import random

class GameObject:
    def __init__(self, width, height, position):
        self.speedx = 0
        self.speedy = 0
        self.height = height
        self.width = width
        self.position = position

    def getEdges(self):
        left = self.position[0] - self.width/2
        top = self.position[1] - self.height/2
        right = self.position[0] + self.width/2
        bottom = self.position[1] + self.height/2
        return (left, top, right, bottom)

    # https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#sidescrollerExamples
    def collidex(self, other):
        (ax0, ay0, ax1, ay1) = self.getEdges()
        (bx0, by0, bx1, by1) = other.getEdges()
        if ((ay1 > other.position[1]-10) and (ay0 < other.position[1]+10)):
            if ((ax1 > bx0) and (bx1 > ax0)):
                # self.speedx -= 2*self.speedx
                return True
        return False

    def collidey(self, other):
        if type(other) == list:
            for element in other:
                (ax0, ay0, ax1, ay1) = self.getEdges()
                (bx0, by0, bx1, by1) = element.getEdges()
                if ((ax1 > bx0) and (bx1 > ax0)):
                    if ((ay1 > by0) and (by1 > ay0)):
                        if ay0 < by0:
                            self.position[1] -= (ay1 - by0)
                            self.speedy = 0
                            self.air = False
                        self.speedy -= 2*self.speedy
                        return element
        return False

class Character(GameObject):
    def __init__(self, width, height, position):
        super().__init__(width, height, position)
        self.air = False
        self.leftBound = 0
        self.rightBound = 0

    def move(self):
        self.position[0] += self.speedx

    def jump(self):
        self.position[1] -= self.speedy
    
    def boundary(self):
        (left, top, right, bottom) = self.getEdges()
        if (left <= self.leftBound) or (right >= self.rightBound):
            self.speedx = -1*self.speedx

class PowerUps(Character):
    def __init__(self, width, height, position, color):
        super().__init__(width, height, position)
        self.held = False
        self.tossed = False
        self.color = color
    
    def picked(self, other):
        if self.collidex(other) or self.collidey([other]):
            return True

    def toss(self, reverse):
        self.tossed = True
        if reverse:
            index = -1
        else:
            index = 1

        self.speedy += 5
        self.speedx += 8*index
    

class Terrain(GameObject):
    def __init__(self, width, height, position, color):
        super().__init__(width, height, position)
        self.color = color

class Vine(GameObject):
    def __init__(self, width, height, position):
        super().__init__(width, height, position)



