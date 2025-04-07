class Section:
    """Section class
    ================
    A class that represents a cross-section of a beam.
    It contains properties such as area, moment of inertia and so on.
    It also contains methods to calculate the section properties and to
    generate a report of the section properties.
    """

    name: str
    """name of the section"""
    A: int
    """area of the section in mm2"""
    Ix: int
    """moment of inertia of the section in mm4 along the x-axis"""
    Iy: int
    """moment of inertia of the section in mm4 along the y-axis"""

    def __init__(self, **properties: dict):
        """initialize the section with the properties"""
        self.name = properties.get("name", "generic")
        self.A = properties.get("A", 0)
        self.Ix = properties.get("Ix", 0)
        self.Iy = properties.get("Iy", 0)
