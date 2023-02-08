"""Special functions.
"""
def range_w_last_val(start: float, end: float, step: float):
    """Adaptation of in-built python `range` function.

    Parameters
    ----------
    start : float
        Start float.
    end : float
        End float.
    step : float
        Step float.

    Yields
    ------
    float
        Range values.
    """
    idx = start
    while idx < end:
        yield idx
        idx = idx + step
    yield end
