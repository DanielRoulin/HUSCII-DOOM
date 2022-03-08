from huscii.renderer import HUSCIIRenderer
import time
import math
import sys
sys.path.append("J:\pymodules")

import keyboard


def dist(x1, y1, x2, y2):
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    return (dx*dx + dy*dy)**0.5

class Ray:
    def __init__(self, r, x, y, dir_x, dir_y):
        self.r = r
        self.x = x
        self.y = y
        self.dir_x = dir_x
        self.dir_y = dir_y
    
    def cast(self, line):
        x1 = line.x1
        y1 = line.y1
        x2 = line.x2
        y2 = line.y2
        
        x3 = self.x
        y3 = self.y
        x4 = self.x + self.dir_x
        y4 = self.y + self.dir_y
        
        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if den == 0:
            return
        
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den
        
        if t > 0 and t < 1 and u > 0:
            x = x1 + t * (x2 -x1)
            y = y1 + t * (y2 -y1)
            return (x, y)
        else:
            return
        
class Line:
    def __init__(self, r, x1, y1, x2, y2):
        self.r = r
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        
    def draw(self):
        self.r.fill_char = "o"
        self.r.line(self.x1, self.y1, self.x2, self.y2)
        
        
class Particle:
    def __init__(self, r):
        self.r = r
        self.x = r.WIDTH/2
        self.y = r.HEIGHT/2
        self.set_rays()
        
    def set_rays(self):
        self.rays = []
        n = 30
        for i in range(n):
            a = (2*math.pi/n) * i
            self.rays.append(Ray(r, self.x, self.y, math.cos(a), math.sin(a)))
            
    def light(self, lines):
        for ray in self.rays:
            mini = math.inf
            pt = None
            for line in lines:
                intersect = ray.cast(line)
                if intersect:
                    d = dist(self.x, self.y, intersect[0], intersect[1])
                    if d < mini:
                        pt = intersect
                        mini = d
            if pt: 
                self.r.fill_char = "."
                self.r.line(ray.x, ray.y, pt[0], pt[1])
                
                
    def draw(self):
        self.r.point(self.x, self.y, "O")
                    
    def update(self, x, y):
        self.x += x
        self.y += y
        self.set_rays()


r = HUSCIIRenderer(width=110, height=50, bg_char = " ")

lines = [
    Line(r, 100, 5, 100, 45),
    Line(r, 10, 5, 10, 45),
    Line(r, 20, 10, 90, 10),
    Line(r, 50, 5, 50, 45),
]

particle = Particle(r)

while True:
    particle.light(lines)
    particle.draw()
    for l in lines:
        l.draw()
        
    if keyboard.is_pressed("s"):
        particle.update(0, 1)
    elif keyboard.is_pressed("w"):
        particle.update(0, -1)
    elif keyboard.is_pressed("d"):
        particle.update(1, 0)
    elif keyboard.is_pressed("a"):
        particle.update(-1, 0)

    r.draw()
    time.sleep(1/30)
    
    
    
    