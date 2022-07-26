def wall_area(wall_side, building_orientation, width_floor, length_floor, height_floor):
    """Compute area

    * width_floor is the dimension of the wall facing the building's building_orientation; e.g. if it faces North, the
      dimension of that North wall is th width; thus the length would from the East/West wall  (building are assumed to
      be rectangular)

    Parameters
    ----------
    wall_side : str
        Wall orientation

    building_orientation : str
        Building orientation

    width_floor : float
        Width [m]

    length_floor : float
        Length [m]

    height_floor : float
        Height [m]

    Returns
    -------
    area : float
        Surface area [m2]

    """

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
