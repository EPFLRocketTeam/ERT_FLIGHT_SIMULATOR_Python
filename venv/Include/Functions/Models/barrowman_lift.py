# Author : Michaël Tasev
# Last update : 16 October 2020
# EPFL Rocket Team, 1015 Lausanne, Switzerland

from Rocket.Rocket import Rocket
import math
import numpy as np


def barrowman_lift(rocket: Rocket, alpha, m, theta):

    a_ref = math.pi * rocket.diameters[1] ** 2 / 4

    # Cone
    if rocket.cone_mode == 'on':
        if alpha == 0:
            CNa_cone = 2
        else:
            CNa_cone = 2 * math.sin(alpha) / alpha
    CP_cone = 2 / 3 * rocket.diameters_position[1]

    # Body
    CNa_stage = np.zeros(1, len(rocket.stages) - 2)
    CP_stage = np.zeros(1, len(rocket.stages) - 2)
    for i in range(len(rocket.stages) - 2):
        if alpha == 0:
            CNa_stage[i] = (rocket.diameters[i + 2] ** 2 - rocket.diameters[i + 1] ** 2) * math.pi / a_ref / 2
        else:
            CNa_stage[i] = ((rocket.diameters[i + 2] ** 2 - rocket.diameters[i + 1] ** 2)
                            * math.pi / a_ref / 2 * math.sin(alpha) / alpha)
        CP_stage[i] = (rocket.diameters_position[i + 1] + 1 / 3 *
                       (rocket.diameters_position[i + 2] - rocket.diameters_position[i + 1]) *
                       (1 + (1 - rocket.diameters[i + 1] / rocket.diameters[i + 2]) / (
                                   1 - (rocket.diameters[i + 1] / rocket.diameters[i + 2]) ** 2)))  # immonde

    # Fins
    if m < 1:
        beta = math.sqrt(1 - m ** 2)
    else:
        print("Warning : in Barrowman calculations Mach number > 1")
        beta = math.sqrt(m ** 2 - 1)

    gamma_c = math.atan(1)
    a = 1
    r = 1
    ktb = 1
    CNa1 = 1
    CNa_fins = 1
    CP_fins = 1  # TODO : change all the above 1s

    # Output
    Calpha = np.append(CNa_stage, CNa_fins)
    CP = np.append(CP_stage, CP_fins)
    if rocket.cone_mode == 'on':
        Calpha = np.append(CNa_cone, Calpha)
        CP = np.append(CP_cone, CP)

    CP[np.where(np.isnan(CP))] = 0

    return np.append(Calpha, CP)
