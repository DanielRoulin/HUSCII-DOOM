import random
import sys
sys.path.append("J:\pymodules")

from huscii.renderer import HUSCIIRenderer
import time
import math
import keyboard
import os


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
        n = 50
        for i in range(n):
            a = (math.pi/2/n) * i
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


def set_env():
    lines = [
        Line(r, 0, 0, 0, r.HEIGHT-1),
        Line(r, 0, r.HEIGHT-1, r.WIDTH-1, r.HEIGHT-1),
        Line(r, r.WIDTH-1, r.HEIGHT-1, r.WIDTH-1, 0),
        Line(r, r.WIDTH-1, 0, 0, 0),
    ]
    for i in range(5):
        x1, x2 = random.randrange(r.WIDTH), random.randrange(r.WIDTH)
        y1, y2 = random.randrange(r.HEIGHT), random.randrange(r.HEIGHT)
        lines.append(Line(r, x1, y1, x2, y2))
    return lines

size = os.get_terminal_size()
r = HUSCIIRenderer(width=size.columns, height=size.lines-3, bg_char = " ")

lines = set_env()

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
        particle.update(2, 0)
    elif keyboard.is_pressed("a"):
        particle.update(-2, 0)
    elif keyboard.is_pressed("r"):
        lines = set_env()

    r.draw()
    time.sleep(1/30)