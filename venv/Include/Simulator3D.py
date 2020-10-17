# Author : Michaël Tasev
# Last update : 16 October 2020
# EPFL Rocket Team, 1015 Lausanne, Switzerland

import numpy as np

from Rocket.Rocket import Rocket
from Functions.Models.stdAtmosUS import stdAtmosUS
from Functions.Models.drag import drag
from Functions.Math.normalize_vector import normalize_vector
from Functions.Math.quat2rotmat import quat2rotmat
from Functions.Math.rot2anglemat import rot2anglemat


class Simulator3D:
    """

    """

    def __init__(self, rocket: Rocket, atmosphere: stdAtmosUS):
        self.x_0 = np.array([0, 0])
        self.t0 = 0
        self.state = [self.x_0]
        self.time = [self.t0]

        self.rocket = rocket
        self.atmosphere = atmosphere

    def rail(self, t, s):
        T = self.rocket.get_thrust(t)
        M = self.rocket.get_mass(t)
        dMdt = self.rocket.get_dmass_dt(t)
        rho = self.atmosphere.get_density(s[0] + self.atmosphere.ground_altitude)
        nu = self.atmosphere.get_viscosity(s[0] + self.atmosphere.ground_altitude)
        a = self.atmosphere.get_speed_of_sound(s[0] + self.atmosphere.ground_altitude)
        # TODO: Add drag influences (done?)
        CD = drag(self.rocket, 0, s[1], nu, a)
        CD_AB = 0  # TODO: Insert reference to drag_shuriken or other
        g = self.atmosphere.G0
        Sm = self.rocket.get_max_cross_section_surface
        return [s[1], T / M - g - s[1] * dMdt / M - 0.5 * rho * Sm * s[1] ** 2 * (CD + CD_AB) / M]

    def flight(self, t, s):
        x = s[0:3]
        v = s[3:6]
        q = s[6:10]
        w = s[10:13]

        # normalise quaternion
        normalize_vector(q)

        # rotation matrix from rocket coordinates to Earth coordinates
        c = quat2rotmat(q)
        angle = rot2anglemat(c)

        # rocket principle frame vectors expressed in Earth coordinates
        ya = c * (1, 0, 0)  # Yaw axis
        pa = c * (0, 1, 0)  # Pitch axis
        ra = c * (0, 0, 1)  # Roll axis

        # Earth coordinates vectors expressed in Earth's frame
        xe = (1, 0, 0)
        ye = (0, 1, 0)
        ze = (0, 0, 1)

        # rocket inertia



    def drogue_parachute(self, t, s):
        x = s[0:3]
        v = s[3:6]

        # not sure if s[2] /!\
        rho = self.atmosphere.get_density(s[2] + self.atmosphere.ground_altitude)

        # aerodynamic force
        v_rel = -v  # TODO add windModel with environment parameters
