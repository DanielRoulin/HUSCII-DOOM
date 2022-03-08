#HuscII Engine collision detection system(c)

class Square():
    
    def Initialize(self, x_ , y_ , w_ , h_):
        self.x = x_
        self.y = y_
        self.width = w_
        self.height = h_
        
    def CheckCollision(self, other):
        
        if(((other.x + other.width) >= self.x > other.x) or ((other.x + other.width) >= (self.x + self.width) >= other.x)): #check for x
            if((other.y >= self.y >= (other.y - other.width)) or (other.y >= (self.y - self.width) >= (other.y - other.width))): #check for y

                if(self.x >= (other.x - other.width)):
                    return "left"
                elif((self.x - self.width) <= other.x):
                    return "right"
                elif(self.y <= (other.y - other.height)):
                    return "up"
                elif((self.y -self.height) >= other.y):
                    return "down"
                
                print("error:// the collision side has not been detected correctly!")
            
        return False
        


    def Debug(self):
        print("Debug: posx: " + str(self.x) + "/ posy: " + str(self.y)+ "/ width: " + str(self.width)+ "/ height: " + str(self.height))

    def Move(self, x_change, y_change):
        self.x = self.x + x_change
        self.y = self.y + y_change
        
    def Resize(self, newW, newH):
        self.width = newW
        self.height = newH

    def Tp(self, newX, newY):
        self.x = newX
        self.y = newY
        

class Border():
    
    def Initialize(self, x_ = 0, y_ = -3, w_ = 80, h_ = 25):
        self.x = x_
        self.y = y_
        self.width = w_
        self.height = h_
        
    def CheckCollision(self, other):
        
        if((other.y - other.height) <= self.y): #coll down
            return "down"
        
        elif(other.y >= (self.y + self.height)): #coll up
            return "up"
        
        elif(other.x <= self.x): #coll left
            return "left"
        
        elif((other.x + other.width) >= (self.x + self.width)): #coll right
            return "right"
        
        else:
            return None
        
    def Resize(self, newW, newH):
        self.width = newW
        self.height = newH
        
    def Tp(self, newX, newY):
        self.x = newX
        self.y = newY


class Ellipse():

    def Initialize(self, x_, y_, w_, h_):
        self.x = x_
        self.y = y_
        self.width = w_
        self.height = h_

    def CheckCollision(self, other):
        
        #TODO #1
        return "this functionality is not yet fully implemented..."
        
    def Resize(self, newW, newH):
        self.width = newW
        self.height = newH
        
    def Tp(self, newX, newY):
        self.x = newX
        self.y = newY



