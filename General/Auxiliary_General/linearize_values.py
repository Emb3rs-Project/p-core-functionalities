def linearize_values(y2, y1, x2, x1):
    """Linearize values

    Get 'a' and 'b' for y = ax+b

    Parameters
    ----------
    y2 : float
        Interpolation value
    y1 : float
        Interpolation value
    x2 : float
        Interpolation value
    x1 : float
        Interpolation value

    Returns
    -------
    a : float
        Interpolation value

    b : float
        Interpolation value

    """

    if x2 - x1 != 0:
        a = (y2 - y1) / (x2 - x1)
        b = y2 - a * x2
    else:
        a = 0
        b = 0

    return a, b
