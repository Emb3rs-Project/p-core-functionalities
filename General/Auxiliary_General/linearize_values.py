"""
alisboa/jmcunha


##############################
INFO: Linearize values
      Get 'a' and 'b' for y = ax+b

##############################
INPUT:
        # values of equation - y2, y1, x2, x1


##############################
RETURN:
        # values of equation - a,b


"""


def linearize_values(y2, y1, x2, x1):

    if x2 - x1 != 0:
        a = (y2 - y1) / (x2 - x1)
        b = y2 - a * x2
    else:
        a = 0
        b = 0

    return a, b
