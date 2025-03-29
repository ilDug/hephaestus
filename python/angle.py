import numpy as np
from fractions import Fraction
import math

def angle_calc(dy, dx):
    if dx == 0 and dy == 0:
        raise ValueError("dx and dy are both 0")

    # analzza i casi in cui dx o dy sono 0          
    if dx == 0 and dy > 0:
        return np.pi / 2
    
    if dx == 0 and dy < 0:
        return (3/2) * np.pi
    
    if dy == 0 and dx > 0:
        return 0
    
    if dy == 0 and dx < 0:
        return np.pi

    # analizza i casi in cui dx o dy sono diversi da 0
    if dx > 0 and dy > 0:  # primo quadrante
        return np.arctan(dy / dx)

    if dx < 0 and dy > 0:  # secondo quadrante
        return np.pi + np.arctan(dy / dx)

    if dx < 0 and dy < 0:  # terzo quadrante
        return np.pi + np.arctan(dy / dx)

    if dx > 0 and dy < 0:  # quarto quadrante
        return 2 * np.pi + np.arctan(dy / dx)


# Example values for dy and dx


for dx, dy in [(1,1), (-1,1), (-1,-1), (1,-1), (0,1), (-1,0), (0,-1), (1,0)]:

    angle =  angle_calc(dy, dx)
    # Convert radians to degrees
    angle_degrees = np.degrees(angle)

    angle_pi_format = f"{angle / np.pi:.2f}π"

    angle_fraction_format = (
        f"{Fraction(angle / np.pi).limit_denominator()}π"
    )



    print (f"Angle in radians: {angle}")
    print(f"Rotation angle in π format: {angle_pi_format}")
    print(f"Rotation angle in π fractional format: {angle_fraction_format}")
    print(f"Angle in degrees: {angle_degrees}")

