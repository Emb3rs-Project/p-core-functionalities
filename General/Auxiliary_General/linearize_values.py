"""
INFO: Linearize values for TEO.
      Get 'a' and 'b' for y = ax+b
"""

def linearize_values(y2,y1,x2,x1):

    if x2-x1 != 0:
        a = (y2 - y1) / (x2-x1)
        b = y2 - a*x2
    else:
        a = 0
        b = 0

    return a,b