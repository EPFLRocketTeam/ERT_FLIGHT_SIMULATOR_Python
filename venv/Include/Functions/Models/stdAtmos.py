from math import exp, sqrt
from scipy.interpolate import interp1d


def stdAtmos(alt, Env):

    """
    Input:  - alt: altitude [m]
            - Env: Environment structure

    Output: - T: Local standard temperature[K]
            - a: local speed of sound[m/s]
            - p: local standard pressure[Pa]
            - rho: local standard density [kg/m^3]
            - Nu: local kinematic viscosity of air [m^2/s]

    ASSUMPTIONS:
     - hydrostatic approximation of atmosphere
     - linear temperature variation with altitude with a slope of -9.5°C/km comes from result of radiosonde data
     - homogenous composition

    LIMITATIONS:
    - troposphere: 10km

     CHECK ALTITUDE RANGE
    """
    if alt > 1e4:
        raise Exception("stdAtmos:outOfRange, The altitude is out of range: max 10km", )

    R = 287.04
    gamma = 1.4
    p0 = 101325
    T0 = 288.15
    a0 = 340.294
    g0 = 9.80665

    # TEMPERATURE MODEL
    T = Env.Temperature_Ground + Env.dTdh * (alt - Env.Start_Altitude) / 1000 # en [K]