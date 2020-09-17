'''see if two images collide'''

def intersectsX(x1,x2,w1,w2):
    if x2 + w2 >= x1 >= x2:
        return True
    if x1 + w1 >= x2 >= x1:
        return True
    return False

def intersectsY(y1,y2,h1,h2):
    if y2 + h2 >= y1 >= y2:
        return True
    if y1 + h1 >= y2 >= y1:
        return True
    return False

def intersects(rectX, rectY):
    if rectX and rectY == True:
        return True
    return False

def intersectsX(x1,x2,w1,w2):
    if x2 + w2 >= x1 >= x2:
        return True
    if x2 + w2 >= x1 + w1 >= x2:
        return True
    return False

'''
def intersectsY(y1,y2,h1,h2):
    if y2 + h2 >= y1 >= y2:
        return True
    if y2 + h2 >= y1 + h1 >= y2:
        return True
    return False

def intersects(rectX, rectY):
    if rectX and rectY == True:
        return True
    return False
'''