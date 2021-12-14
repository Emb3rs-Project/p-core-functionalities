"""
alisboa/jmcunha


##############################
INFO: get interpolation value

      y = ax+b
      a = (y2-y1)/(x2-x1)

##############################
INPUT:
        # values for equation - y2,y1,x2,x1,x,b


##############################
RETURN:
        # value desired to be obtained -  y


"""


def interpolation(y2, y1, x2, x1, x, b):
    y = (y2 - y1) / (x2 - x1) * x + b

    return y
