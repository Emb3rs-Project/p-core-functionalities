""""

Info: Compute Building's wall or glass area.
      width_floor is the dimension of the wall facing the building_orientation of the building
      For wall, ratio = ratio_wall
      For glass, ratio = ratio_glass

"""

def wall_area(wall_side,building_orientation,width_floor,length_floor,height_floor):

    if building_orientation == 'N' or building_orientation == 'S':
        if wall_side == 'N' or wall_side == 'S':
            area = width_floor * height_floor  # [m2]
        else:
            area = length_floor * height_floor  # [m2]
    else:
        if wall_side == 'N' or wall_side == 'S':
            area = length_floor * height_floor  # [m2]
        else:
            area = width_floor * height_floor  # [m2]


    return area
