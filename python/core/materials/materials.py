from typing import TypedDict, Protocol
from dataclasses import dataclass


# @dataclass
class Material(Protocol):
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
    """name of the material"""
    group: str  # group of the material
    """group of the material"""
    rho: float  # density [kg/m^3]
    """density [kg/m^3]"""
    E: int  # Young's modulus [MPa]
    """Young's modulus [MPa]"""
    nu: float  # Poisson's ratio [adm]
    """Poisson's ratio [adm]"""
    G: int  # shear modulus [MPa]
    """shear modulus [MPa]"""
    alpha: float  # thermal expansion coefficient [1/K]
    """thermal expansion coefficient [1/K]"""
    k: float  # thermal conductivity [W/(m·K)]
    """thermal conductivity [W/(m·K)]"""
    cp: float  # specific heat capacity [J/(kg·K)]
    """specific heat capacity [J/(kg·K)]"""
    fy: int  # yield strength [MPa]
    """yield strength [MPa]"""
    fu: int  # ultimate strength [MPa]
    """ultimate strength [MPa]"""


class Steel:
    """
    Steel class
    Attributes:
        name (str): Name of the steel.
        group (str): Group of the steel.
        rho (float): Density of the steel in kg/m^3.
        E (int): Young's modulus in MPa.
        nu (float): Poisson's ratio.
        G (int): Shear modulus in MPa.
        alpha (float): Thermal expansion coefficient in 1/K.
        k (float): Thermal conductivity in W/(m·K).
        cp (float): Specific heat capacity in J/(kg·K).
        fy (int): Yield strength in MPa.
        fu (int): Ultimate strength in MPa.
    """

    name: str = "Steel"
    """name of the steel"""
    group: str = "Steel"
    """group of the steel"""
    rho: float = 7850  # density [kg/m^3]
    """density [kg/m^3]"""
    E: int = 210000  # Young's modulus [MPa]
    """Young's modulus [MPa]"""
    nu: float = 0.3  # Poisson's ratio [adm]
    """Poisson's ratio [adm]"""
    G: int = 81000  # shear modulus [MPa]
    """shear modulus [MPa]"""
    alpha: float = 1.2e-5  # thermal expansion coefficient [1/K]
    """thermal expansion coefficient [1/K]"""
    k: float = 50  # thermal conductivity [W/(m·K)]
    """thermal conductivity [W/(m·K)]"""
    cp: float = 500  # specific heat capacity [J/(kg·K)]
    """specific heat capacity [J/(kg·K)]"""


class S235(Steel):
    fy: float = 235  # yield strength [MPa]
    """yield strength [MPa]"""
    fu: float = 360  # ultimate strength [MPa]
    """ultimate strength [MPa]"""


class S275(Steel):
    fy: float = 275  # yield strength [MPa]
    """yield strength [MPa]"""
    fu: float = 430  # ultimate strength [MPa]
    """ultimate strength [MPa]"""


class S355(Steel):
    fy: float = 355  # yield strength [MPa]
    """yield strength [MPa]"""
    fu: float = 490  # ultimate strength [MPa]
    """ultimate strength [MPa]"""


class S450(Steel):
    fy: float = 440  # yield strength [MPa]
    """yield strength [MPa]"""
    fu: float = 550  # ultimate strength [MPa]
    """ultimate strength [MPa]"""
