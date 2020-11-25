# Author : Michaël Tasev
# Last update : 16 October 2020
# EPFL Rocket Team, 1015 Lausanne, Switzerland

import numpy as np
import numpy.linalg as lin
import math
from scipy.integrate import ode, solve_ivp

from Rocket.Stage import Stage
from Rocket.Rocket import Rocket
from Rocket.Body import Body
from Functions.Models.stdAtmosUS import stdAtmosUS
from Functions.Models.drag import drag
from Functions.Models.drag_shuriken import drag_shuriken
from Functions.Models.wind_model import wind_model
from Functions.Models.normal_lift import normal_lift
from Functions.Models.pitch_damping_moment import pitch_damping_moment
from Functions.Math.normalize_vector import normalize_vector
from Functions.Math.quat2rotmat import quat2rotmat
from Functions.Math.rot2anglemat import rot2anglemat
from Functions.Math.quat_evolve import quat_evolve
from Functions.Models.pitch_damping_moment import pitch_damping_moment


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

        # Normalise quaternion
        normalize_vector(q)

        # Rotation matrix from rocket coordinates to Earth coordinates
        c = quat2rotmat(q)
        angle = rot2anglemat(c)

        # Rocket principle frame vectors expressed in Earth coordinates
        ya = c * np.array([1, 0, 0]).transpose()  # Yaw axis
        pa = c * np.array([0, 1, 0]).transpose()  # Pitch axis
        ra = c * np.array([0, 0, 1]).transpose()  # Roll axis

        # Earth coordinates vectors expressed in Earth's frame
        xe = np.array([1, 0, 0]).transpose()
        ye = np.array([0, 1, 0]).transpose()
        ze = np.array([0, 0, 1]).transpose()

        # Rocket inertia and properties
        m = self.rocket.get_mass(t)
        dMdt = self.rocket.get_dmass_dt(t)
        cg = self.rocket.get_cg(t)
        Sm = self.rocket.get_max_cross_section_surface
        I_L = self.rocket.get_long_inertia(t)
        I_R = self.rocket.get_rot_inertia(t)
        I = c.transpose() * ([[I_L, 0, 0],
                              [0, I_L, 0],
                              [0, 0, I_R]]) * c

        # Environment
        g = 9.81  # Gravity [m/s^2]
        rho = self.atmosphere.get_density(x[0] + self.atmosphere.ground_altitude)
        nu = self.atmosphere.get_viscosity(x[0] + self.atmosphere.ground_altitude)
        a = self.atmosphere.get_speed_of_sound(x[0] + self.atmosphere.ground_altitude)

        # Thrust
        # Oriented along roll axis of rocket frame, expressed, in earth coordinates
        T = self.rocket.get_thrust(t) * ra

        # Gravity
        G = -g * m * ze

        # Aerodynamic corrective forces
        # Compute center of mass angle of attack
        v_cm = v - wind_model(t, self.atmosphere.get_turb(x[0] + self.atmosphere.ground_altitude),
                              self.atmosphere.get_v_inf(), self.atmosphere.get_turb_model(), x[2])
        v_cm_mag = np.linalg.norm(v_cm)
        alpha_cm = math.atan2(np.linalg.norm(np.cross(ra, v_cm)), np.dot(ra, v_cm))

        # Mach number
        Mach = np.linalg.norm(v_cm_mag) / a

        # Normal lift coefficient and center of pressure
        CNa, Xcp, CNa_bar, CP_bar = normal_lift(self.rocket, alpha_cm, 1.1, Mach, angle[2], 1)

        # Stability margin
        margin = Xcp - cg

        # Compute rocket angle of attack
        if np.linalg.norm(w) != 0:
            w_norm = w / np.linalg.norm(w)
        else:
            w_norm = np.zeros(3, 1)

        v_rel = v_cm + margin * math.sin(math.acos(np.dot(ra, w_norm))) * np.cross(ra, w)
        v_mag = np.linalg.norm(v_rel)
        v_norm = normalize_vector(v_rel)

        # Angle of attack
        v_cross = np.cross(ra, v_norm)
        v_cross_norm = normalize_vector(v_cross)
        alpha = math.atan2(np.linalg.norm(np.cross(ra, v_norm)), np.dot(ra, v_norm))
        delta = math.atan2(np.linalg.norm(np.cross(ra, ze)), np.dot(ra, ze))

        # Normal force
        na = np.cross(ra, v_cross)
        if np.linalg.norm(na) == 0:
            n = np.array([0, 0, 0]).transpose
        else:
            n = 0.5 * rho * Sm * CNa * alpha * v_mag ** 2 * na / np.linalg.norm(na)

        # Drag
        # Drag coefficient
        cd = drag(self.rocket, alpha, v_mag, nu, a)  # TODO : * cd_fac (always 1 ?)
        ab_phi = -230  # TODO : find a way to deal with airbrakes, /!\ magic number
        if t > self.rocket.get_burn_time:
            cd = cd + drag_shuriken(self.rocket, ab_phi, alpha, v_mag, nu)

        # Drag force
        d = -0.5 * rho * Sm * cd * v_mag ** 2 * v_norm

        # Total forces
        motor_fac = 1  # TODO : always 1 ?
        f_tot = T * motor_fac + G + n + d

        # Moment estimation

        # Aerodynamic corrective moment
        mn = np.linalg.norm(n) * margin * v_cross_norm

        # Aerodynamic damping moment
        w_pitch = w - np.dot(w, ra) * ra
        cdm = pitch_damping_moment(self.rocket, rho, CNa_bar, CP_bar, dMdt, cg, np.linalg.norm(w_pitch), v_mag)
        md = -0.5 * rho * cdm * Sm * v_mag ** 2 * normalize_vector(w_pitch)

        m_tot = mn + md

        # State derivatives
        q_dot = quat_evolve(q, w)
        w_dot = lin.lstsq(I, m_tot)

        return [v, 1 / m * (f_tot - v * dMdt), q_dot, w_dot]

    def drogue_parachute(self, t, s, rocket, m):
        x = s[0:3]
        v = s[3:6]

        rho = self.atmosphere.get_density(x[2] + self.atmosphere.ground_altitude)

        # Aerodynamic force
        v_rel = -v + wind_model(t, self.atmosphere.get_turb(x[0] + self.atmosphere.ground_altitude),
                              self.atmosphere.get_v_inf(), self.atmosphere.get_turb_model(), x[2])
        SCD = 1  # TODO : check SCD meaning : surface du parachute * coefficient de drag (= cd)
        d = 0.5 * rho * SCD * np.linalg.norm(v_rel) * v_rel

        # Gravity force
        g = 9.81 * np.array(0, 0, -1).transpose()
        G = g * m

        return [v, (d + G) / m]

    def get_integration(self, number_of_steps: float, max_time: float):

        def off_rail(t, y): return y[0] - 5

        off_rail.terminal = True
        off_rail.direction = 1

        def apogee(t, y): return y[1]

        apogee.terminal = True
        apogee.direction = -1

        self.integration_ivp = solve_ivp(self.rail, [self.t0, max_time], self.x_0, method='RK45', event=off_rail)

        self.integration_ivp = solve_ivp(self.flight, [self.integration_ivp.t[-1], max_time],
                                         self.integration_ivp.y[:, -1], method='RK45', events=apogee)

        self.integration_ivp = solve_ivp(self.drogue_parachute, [self.integration_ivp.t[-1], max_time],
                                         self.integration_ivp.y[:, -1], method='RK45')


if __name__ == '__main__':
    # Rocket definition
    gland = Body("tangent ogive", [0, 0.125], [0, 0.505])
