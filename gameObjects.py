import random

class object:
    def __init__(self, height, width, position):
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
        for element in other:
            (ax0, ay0, ax1, ay1) = self.getEdges()
            (bx0, by0, bx1, by1) = element.getEdges()
            if ((ax1 > bx0) and (bx1 > ax0)):
                if ((ay1 > by0) and (by1 > ay0)):
                    if ay0 < by0:
                        self.position[1] -= (ay1 - by0)
                        self.speedy = 0
                        self.air = False
                    # if by1 > ay0:
                    self.speedy -= 2*self.speedy
                    return True
        return False


class hero(object):
    def __init__(self, height, width, position):
        super().__init__(height, width, position)
        self.air = False

    def move(self):
        self.position[0] += self.speedx
    def jump(self):
        self.position[1] -= self.speedy
        

class terrain(object):
    def __init__(self, height, width, position):
        super().__init__(height, width, position)
    

