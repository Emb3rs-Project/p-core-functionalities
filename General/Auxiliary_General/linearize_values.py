"""
INFO: Linearize values for TEO.
      Get 'a' and 'b' for y = ax+b
"""

def linearize_values(y2,y1,x2,x1):

    a = (y2 - y1) / (x2-x1)

    b = y2 - a*x2

    return a,b