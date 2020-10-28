# Author : Michaël Tasev
# Last update : 16 October 2020
# EPFL Rocket Team, 1015 Lausanne, Switzerland

import numpy as np
import math

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
        m = self.rocket.get_mass(t)
        dMdt = self.rocket.get_dmass_dt(t)
        rho = self.atmosphere.get_density(s[0] + self.atmosphere.ground_altitude)
        nu = self.atmosphere.get_viscosity(s[0] + self.atmosphere.ground_altitude)
        a = self.atmosphere.get_speed_of_sound(s[0] + self.atmosphere.ground_altitude)
        # TODO: Add drag influences (done?)
        CD = drag(self.rocket, 0, s[1], nu, a)
        CD_AB = 0  # TODO: Insert reference to drag_shuriken or other
        g = self.atmosphere.G0
        Sm = self.rocket.get_max_cross_section_surface
        return [s[1], T / m - g - s[1] * dMdt / m - 0.5 * rho * Sm * s[1] ** 2 * (CD + CD_AB) / m]

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
        m = self.rocket.get_mass(t)
        dMdt = self.rocket.get_dmass_dt(t)
        # TODO : add center of mass (add_cg), longitudinal moment of inertia (I_L), rotational moment of inertia (I_R)

        # Environment
        g = 9.81  # Gravity [m/s^2]
        rho = self.atmosphere.get_density(s[0] + self.atmosphere.ground_altitude)
        nu = self.atmosphere.get_viscosity(s[0] + self.atmosphere.ground_altitude)
        a = self.atmosphere.get_speed_of_sound(s[0] + self.atmosphere.ground_altitude)

        # Thrust
        # Oriented along roll axis of rocket frame, expressed, in earth coordinates
        T = self.rocket.get_thrust(t) * ra

        # Gravity
        G = -g * m * ze

        # Aerodynamic corrective forces
        # Compute center of mass angle of attack
        # TODO
        v_cm = v  # -windModel
        # v_cm_mag = ...
        # alpha_cm = ...

        # Mach number
        Mach = np.linalg.norm(v) / a  # TODO : replace v with v_cm_mag when the above TODO is completed

        # Normal lift coefficient and center of pressure
        # TODO : normalLift function, implies doing Barrowmanlift and stuff
        CNa = 0  # TODO : update
        #

        # Stability margin
        # TODO
        # margin = x_cp - cg

        # Compute rocket angle of attack
        if np.linalg.norm(w) != 0:
            w_norm = w / np.linalg.norm(w)
        else:
            w_norm = np.zeros(3, 1)
        v_rel = v_cm  # TODO : + margin * sin(acos(dot(ra, w_norm))) * cross(ra, w)
        v_mag = np.linalg.norm(v_rel)
        v_norm = normalize_vector(v_rel)

        # Angle of attack
        v_cross = np.cross(ra, v_norm)
        v_cross_norm = normalize_vector(v_cross)
        alpha = math.atan2(np.linalg.norm(np.cross(ra, v_norm)), np.dot(ra, v_norm))
        delta = math.atan2(np.linalg.norm(np.cross(ra, ze)), np.dot(ra, ze))

        Sm = 0  # TODO : import from rocketReader, then delete this line
        # normal force
        na = np.cross(ra, v_cross)
        if np.linalg.norm(na) == 0:
            n = (0, 0, 0)
        else:
            n = 0.5 * rho * Sm * CNa * alpha * v_mag ** 2 * na / np.linalg.norm(na)

        # Drag
        # Drag coefficient
        cd = drag(Rocket, alpha, v_mag, nu, a)  # TODO : * cd_fac (to import from rocketReader)
        # TODO : add if t > burn_time then add drag_shuriken

        # Drag force
        d = -0.5 * rho * Sm * cd * v_mag**2 * v_norm

        # Total forces
        motor_fac = 0  # TODO : import from rocketReader
        f_tot = T * motor_fac + G + n + d

        # Moment estimation

        # Aerodynamic corrective moment
        mn = np.linalg.norm(n) * v_cross_norm  # TODO : * margin

        # Aerodynamic damping moment
        w_pitch = w - np.dot(w, ra) * ra
        cdm = 1  # TODO : pitchDampingMoment
        md = -0.5 * rho * cdm * Sm * v_mag**2 * normalize_vector(w_pitch)

        m_tot = mn + md

        # State derivatives
        # TODO : quat_evolve
        q_dot = 1
        w_dot = 1

        return [v, 1/m*(f_tot - v*dMdt), q_dot, w_pitch]  # TODO : q_dot = quat_evolve(q, w), w_dot = I \ m_tot


    def drogue_parachute(self, t, s, rocket, environment, m, main):
        x = s[0:3]
        v = s[3:6]

        # not sure if s[2] /!\
        rho = self.atmosphere.get_density(s[2] + self.atmosphere.ground_altitude)

        # aerodynamic force
        v_rel = -v  # TODO : add windModel with environment parameters
        SCD = 0  # TODO : import from rocketReader
        d = 0.5 * rho * SCD * np.linalg.norm(v_rel) * v_rel

        # Gravity force
        g = 9.81 * (0, 0, -1)
        G = g * m

        return [v, (d + G) / m]
