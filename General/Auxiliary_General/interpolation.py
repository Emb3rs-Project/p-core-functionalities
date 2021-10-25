
"""
y = ax+b
    a = (y2-y1)/(x2-x1)

"""
def interpolation(y2,y1,x2,x1,x,b):

    y = (y2 - y1) / (x2-x1) * x + b

    return y