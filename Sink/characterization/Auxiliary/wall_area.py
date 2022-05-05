"""
alisboa/jmcunha


##############################
INFO: Compute wall/glass area.

      * width_floor is the dimension of the wall facing the building's building_orientation; e.g. if it faces North, the
      dimension of that North wall is th width; thus the length would from the East/West wall  (building are assumed to
      be rectangular)

      * For the wall, ratio = ratio_wall
        For the glass, ratio = ratio_glass


##############################
INPUT:
        # wall_side - e.g. 'N','S','E' or 'W'
        # building_orientation - e.g. 'N','S','E' or 'W'
        # width_floor  [m]
        # length_floor [m]
        # height_floor [m]


##############################
OUTPUT:
        # area  [m2]


"""


def wall_area(wall_side, building_orientation, width_floor, length_floor, height_floor):

    if building_orientation == 'N' or building_orientation == 'S':
        if wall_side == 'N' or wall_side == 'S':
            area = width_floor * height_floor
        else:
            area = length_floor * height_floor
    else:
        if wall_side == 'N' or wall_side == 'S':
            area = length_floor * height_floor
        else:
            area = width_floor * height_floor

    return area
