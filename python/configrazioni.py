import numpy as np

def point_load_fixed_fixed(x:int, P:float ):
    l = 1000
    a = x
    b = l - a

    Ti =  +((P * b**2) /(l**3)) * (l + 2 * a)
    Mi =  +(P * a * b**2) /l**2
    Tj =  +((P * a**2) /(l**3)) * (l + 2 * b)
    Mj =  -(P * a**2 * b) /l**2

def point_load_fixed_hinged(x:int, P:float ):
    l= 1000
    a = x
    b = l - a

    Ti = +((P * b) /(2 * l)) * (3 - (b**2 / l**2))
    Mi = +((P * a * b) / (2 * l**2)) * (l + b)
    Tj = +((P * a**2) / (2 * l**3)) * (2 * l + b)
    Mj = 0

def point_load_hinged_fixed(x:int, P:float ):
    l = 1000
    a = x
    b = l - a

    Ti = +((P * b**2) / (2 * l**3)) * (2 * l + a)
    Mi = 0
    Tj = +((P * a) / (2 * l)) * (3 - (a**2 / l**2))
    Mj = -((P * b * a) / (2 * l**2)) * (l + a)


def point_load_hinged_hinged(x:int, P:float ):
    l = 1000
    a =     x  
    b = l - a

    Ti = +P * b / l
    Mi = 0
    Tj = +P * a / l
    Mj = 0


# def momentum_fixed_fixed(x:int, M:float ):
#     l = 1000
#     a = x
#     b = l - a

#     Ti = -6 * M  * a * b / l**3
#     Mi = - M * b / l * (2 - 3 * b / l)
#     Tj = +6 * M * a * b / l**3
#     Mj = -M * a / l * (2 - 3 * a / l)


# def momentum_fixed_hinged(x:int, M:float ):
#     l = 1000
#     a = x
#     b = l - a

#     Ti = 0
#     Mi = 0
#     Tj = 0
#     Mj = 0
