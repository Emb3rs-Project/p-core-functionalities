def interpolation(y2, y1, x2, x1, x, b):
    """Get interpolation value

    y = ax+b
    a = (y2-y1)/(x2-x1)

    Parameters
    ----------
    y2 : float
        Value for interpolation

    y1 : float
        Value for interpolation

    x2 : float
        Value for interpolation

    x1 : float
        Value for interpolation

    x : float
        Value for interpolation

    b : float
        Value for interpolation


    Returns
    -------
    y : float
        Interpolation result
    """

    y = (y2 - y1) / (x2 - x1) * x + b

    return y
