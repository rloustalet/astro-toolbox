"""This module contains function to parse str
"""
import re
def angle_parser(str_angle):
    """string angle parser

    Parameters
    ----------
    str_anle : str
        The angle value as str in format ()

    Returns
    -------
    _type_
        _description_
    """
    angle_list =  re.split(r"[\-:°'\"hms]",str_angle)
    if len(angle_list) == 1 and "." in angle_list[0]:
        return float(angle_list[0])
    angle = [int(val) for val in angle_list]
    if len(angle) == 3:
        angle[-1] = float(angle_list[-1])
    return tuple(angle)
