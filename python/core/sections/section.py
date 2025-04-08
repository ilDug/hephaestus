from pydantic import BaseModel


class Section(BaseModel):
    """Section
    ================
    A class that represents a cross-section of a beam.
    """

    profile: str
    """name of the section"""
    g: float
    """peso lineare del profilo in kg/m"""

    h: int
    """height of the section in mm"""
    b: int
    """width of the section in mm"""
    tw: int
    """spessore dell'anima in mm"""
    tf: int
    """spessore delle flange/ali in mm"""
    r: int
    """raggio di raccordo in mm"""

    A: int
    """area of the section in mm^2"""

    Iy: int
    """moment of inertia of the section in mm^4 along main axis"""
    iy: float
    """radius of gyration of the section in mm along main axis"""
    Wely: float
    """Elastic section modulus of the section in mm^3 along main axis"""
    Wply: float
    """Plastic section modulus of the section in mm^3 along main axis"""

    Iz: int
    """moment of inertia of the section in mm^4 along the trasverse axis"""
    iz: float
    """radius of gyration of the section in mm along the trasverse axis"""
    Welz: float
    """Elastic section modulus of the section in mm^3 along the trasverse axis"""
    Wplz: float
    """Plastic section modulus of the section in mm^3 along the trasverse axis"""

    J: int
    """torsional constant of the section in mm^4"""
    Cw: int
    """Warping constant in mm6 (costante di deformazione torsionale)"""
