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
    def __init__(self, r, x, y, fov, angle):
        self.r = r
        self.x = x
        self.y = y
        self.fov = fov
        self.angle = angle
        self.set_rays()
        
    def set_rays(self):
        self.rays = []
        for i in range(self.fov):
            a = math.radians(i + self.angle)
            self.rays.append(Ray(r, self.x, self.y, math.cos(a), math.sin(a)))
            
    def cast(self, lines):
        dists = []
        for ray in self.rays:
            mini = math.inf
            for line in lines:
                intersect = ray.cast(line)
                if intersect:
                    d = dist(self.x, self.y, intersect[0], intersect[1])
                    mini = min(d, mini)
            dists.append(mini)
        return dists
    
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
        
        self.r.point(self.x, self.y, "X")
                
    def rotate(self, angle):
        self.angle += angle
        self.set_rays()
                    
    def translate(self, x, y):
        self.x += x
        self.y += y
        self.set_rays()


# size = os.get_terminal_size()
r = HUSCIIRenderer(110, 50, bg_char = " ")

lines = [
    Line(r, 0, 0, 0, r.HEIGHT/2),
    Line(r, 0, r.HEIGHT/2, r.WIDTH, r.HEIGHT/2),
    Line(r, r.WIDTH-1, r.HEIGHT/2, r.WIDTH-1, 0),
    Line(r, r.WIDTH, 0, 0, 0),

    Line(r, 100, 5, 80, 15),
    Line(r, 10, 5, 10, 10),
    Line(r, 20, 10, 90, 10),
    Line(r, 50, 10, 50, 20),
]

particle = Particle(r, round(r.WIDTH/2), round(r.HEIGHT/4), 40, 0)

while True:        
    if keyboard.is_pressed("s"):
        particle.translate(0, 1)
    elif keyboard.is_pressed("w"):
        particle.translate(0, -1)
    elif keyboard.is_pressed("d"):
        particle.translate(2, 0)
    elif keyboard.is_pressed("a"):
        particle.translate(-2, 0)
        
    elif keyboard.is_pressed("q"):
        particle.rotate(2)
    elif keyboard.is_pressed("e"):
        particle.rotate(-2)
    
        
    particle.light(lines)
    
    for l in lines:
        l.draw()
    
    dists = particle.cast(lines)
    width = r.WIDTH/len(dists)
    x = 0
    for i, d in enumerate(dists):
        height = r.HEIGHT/2 - (d/50 * r.HEIGHT/2)
        brightness = 9 - min(9, round(d/50 * 10))
        r.fill_char = r.CHARS[brightness]
        r.rect(x, r.HEIGHT/4*3 - height/2, width, height)
        x += width

    r.draw()
    time.sleep(1/30)
