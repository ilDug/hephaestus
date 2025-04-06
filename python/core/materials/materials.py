from typing import TypedDict
from dataclasses import dataclass

# @dataclass
class Material(TypedDict): 
    """
        MAterial Base class
        Attributes:
            name (str): Name of the material.
            rho (float): Density of the material in kg/m^3.
            E (int): Young's modulus in MPa.
            nu (float): Poisson's ratio.
            G (int): Shear modulus in MPa.
            alpha (float): Thermal expansion coefficient in 1/K.
            k (float): Thermal conductivity in W/(m·K).
            cp (float): Specific heat capacity in J/(kg·K).
            fy (int): Yield strength in MPa.
            fu (int): Ultimate strength in MPa.
    """
    name: str  # name of the material
    group: str  # group of the material
    rho: float  # density [kg/m^3]
    E: int  # Young's modulus [MPa]
    nu: float  # Poisson's ratio [adm]
    G: int  # shear modulus [MPa]
    alpha: float  # thermal expansion coefficient [1/K]
    k: float  # thermal conductivity [W/(m·K)]
    cp: float  # specific heat capacity [J/(kg·K)]
    fy: int  # yield strength [MPa]
    fu: int  # ultimate strength [MPa]


STEELS = {
    "S235": {
        "name": "S235",
        "group": "Steel",
        "rho": 7850,  # density [kg/m^3]
        "E": 210000,  # Young's modulus [MPa]
        "nu": 0.3,  # Poisson's ratio [adm]
        "G": 81000,  # shear modulus [MPa]
        "alpha": 1.2e-5,  # thermal expansion coefficient [1/K]
        "k": 50,  # thermal conductivity [W/(m·K)]
        "cp": 500,  # specific heat capacity [J/(kg·K)]
        "fy": 235,  # yield strength [MPa]
        "fu": 360,  # ultimate strength [MPa]
    },
    "S275": {
        "name": "S275",
        "group": "Steel",
        "rho": 7850,
        "E": 210000,
        "nu": 0.3,
        "G": 81000,
        "alpha": 1.2e-5,
        "k": 50,
        "cp": 500,
        "fy": 275,
        "fu": 430,
    },
    "S355": {
        "name": "S355",
        "group": "Steel",
        "rho": 7850,
        "E": 210000,
        "nu": 0.3,
        "G": 81000,
        "alpha": 1.2e-5,
        "k": 50,
        "cp": 500,
        "fy": 355,
        "fu": 490,
    },
    "S450": {
        "name": "S450",
        "group": "Steel",
        "rho": 7850,
        "E": 210000,
        "nu": 0.3,
        "G": 81000,
        "alpha": 1.2e-5,
        "k": 50,
        "cp": 500,
        "fy": 440,
        "fu": 550,
    }
}

