# Author : Michaël Tasev
# Last update : 16 October 2020
# EPFL Rocket Team, 1015 Lausanne, Switzerland

import numpy as np


def quat2rotmat(q):
    """

    Parameters
    ----------
    q           : the quaternion representing the attitude of the vehicle in earth's cartesian coordinate system.

    Returns
    -------
    A 3x3 matrix that rotates the coordinate system proper to the vehicle into earth's coordinate system

    Notes
    -----
    https://www.euclideanspace.com/maths/geometry/rotations/conversions/quaternionToMatrix/index.htm

    """

    return np.reshape([
        1 - 2 * q[1] ** 2 - 2 * q[2] ** 2,
        2 * (q[0] * q[1] + q[2] * q[3]),
        2 * (q[0] * q[2] - q[1] * q[3]),
        2 * (q[0] * q[1] - q[2] * q[3]),
        1 - 2 * q[0] ** 2 - 2 * q[2] ** 2,
        2 * (q[1] * q[2] + q[0] * q[3]),
        2 * (q[0] * q[2] + q[1] * q[3]),
        2 * (q[1] * q[2] - q[0] * q[3]),
        1 - 2 * q[0] ** 2 - 2 * q[1] ** 2], [3, 3], order='F')
