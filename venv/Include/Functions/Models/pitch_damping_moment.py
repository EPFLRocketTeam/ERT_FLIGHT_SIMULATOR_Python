# Author : Michaël Tasev
# Last update : 16 October 2020
# EPFL Rocket Team, 1015 Lausanne, Switzerland

from Rocket.Rocket import Rocket
import numpy as np


def pitch_damping_moment(rocket: Rocket, rho, calpha, CP, dMdt, cg, w, v):
    """

    Parameters
    ----------
    rocket          : Rocket object
    rho             : air resistance
    calpha          : normal lift coefficient derivatives
    CP              : center of pressure
    dMdt            : mass change rate
    cg              : center of gravity
    w               : angular velocity of the rocket, as a scalar
    v               : velocity of the rocket, as a scalar

    Returns
    -------
    cdm             : the pitch damping moment coefficient of the rocket, which also applies to yaw
                      damping but not to roll

    """

    cdm = 0

    if v != 0:
        cdm_thrust = dMdt * (rocket.get_length - cg) ** 2 * w * 2 / (v**2 * rho * rocket.get_max_cross_section_surface)
        CNa_Total = np.sum(calpha*(CP-cg)**2)
        cdm_aero = CNa_Total*w/v

        cdm = cdm_aero + cdm_thrust

    return cdm
