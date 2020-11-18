# Motor class file
# Author : Jules Triomphe
# Date : 5 May 2019
# EPFL Rocket Team, 1015 Lausanne, Switzerland

import numpy as np
from scipy.integrate import ode, solve_ivp

from Rocket.Body import Body
from Rocket.Rocket import Rocket
from Rocket.Stage import Stage
from Functions.stdAtmosUS import stdAtmosUS
from Functions.drag import drag


class Simulator1D:
    """

    """

    def __init__(self, rocket: Rocket, atmosphere: stdAtmosUS):
        self.x_0 = np.array([0, 0])
        self.t0 = 0
        self.state = [self.x_0]
        self.time = [self.t0]

        self.rocket = rocket
        self.atmosphere = atmosphere

    def xdot(self, t, x):
        T = self.rocket.get_thrust(t)
        M = self.rocket.get_mass(t)
        dMdt = self.rocket.get_dmass_dt(t)
        rho = self.atmosphere.get_density(x[0] + self.atmosphere.ground_altitude)
        nu = self.atmosphere.get_viscosity(x[0] + self.atmosphere.ground_altitude)
        a = self.atmosphere.get_speed_of_sound(x[0] + self.atmosphere.ground_altitude)
        # TODO: Add drag influences (done?)
        CD = drag(self.rocket, 0, x[1], nu, a)
        CD_AB = 0  # TODO: Insert reference to drag_shuriken or other
        g = self.atmosphere.G0
        Sm = self.rocket.get_max_cross_section_surface
        return [x[1], T / M - g - x[1] * dMdt / M - 0.5 * rho * Sm * x[1] ** 2 * (CD + CD_AB) / M]

    def get_integration(self, number_of_steps: float, max_time: float):
        """self.time_span = np.linspace(self.t0, max_time, number_of_steps)
        self.time_step = self.time_span[1] - self.time_span[0]
        self.integration = ode(self.xdot).set_integrator('dopri5').set_initial_value(self.x_0, self.t0)"""

        def off_rail(t, y): return y[0] - 5

        off_rail.terminal = True
        off_rail.direction = 1

        def apogee(t, y): return y[1]

        apogee.terminal = True
        apogee.direction = -1

        import matplotlib.pyplot as plt

        self.integration_ivp = solve_ivp(self.xdot, [self.t0, max_time], self.x_0, method='RK45', events=off_rail)
        print('Solve_ivp rail')
        print("t", self.integration_ivp.t)
        print("y", self.integration_ivp.y)

        plt.plot(self.integration_ivp.t, self.integration_ivp.y[0])
        plt.show()

        self.integration_ivp = solve_ivp(self.xdot, [self.integration_ivp.t[-1], max_time],
                                         self.integration_ivp.y[:, -1], method='RK45', events=apogee)
        print('Solve_ivp ascent')
        print(self.integration_ivp.t)
        print(self.integration_ivp.y)

        plt.plot(self.integration_ivp.t, self.integration_ivp.y[0])
        plt.show()

        self.time_span = np.linspace(self.t0, max_time, number_of_steps)
        self.time_step = self.time_span[1] - self.time_span[0]
        self.integration = ode(self.xdot).set_integrator('dopri5').set_initial_value(self.x_0, self.t0)
        self.integration.integrate(self.integration.t + self.time_step)
        self.time.append(self.integration.t)
        self.state.append(self.integration.y)
        while self.integration.successful() and self.integration.y[1] > 0:
            print(self.integration.t + self.time_step, self.integration.integrate(self.integration.t + self.time_step))
            self.time.append(self.integration.t)
            self.state.append(self.integration.y)
        return


if __name__ == '__main__':
    # Rocket definition
    gland = Body("tangent ogive", [0, 0.125], [0, 0.505])

    tubes_francais = Body("cylinder", [0.125, 0.125, 0.102], [0, 1.85, 1.9])

    M3_cone = Stage('Matterhorn III nosecone', gland, 1.26, 0.338, np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]]))

    M3_body = Stage('Matterhorn III body', tubes_francais, 9.6, 0.930,
                    np.array([[2.72, 0, 0], [0, 2.72, 0], [0, 0, 0]]))

    finDefData = {'number': 3,
                  'root_chord': 0.236,
                  'tip_chord': 0.118,
                  'span': 0.128,
                  'sweep': 0.06,
                  'thickness': 0.003,
                  'phase': 0,
                  'body_top_offset': 1.585,
                  'total_mass': 0.3}

    M3_body.add_fins(finDefData)

    M3_body.add_motor('Motors/AT_L850.eng')

    Matterhorn_III = Rocket()

    Matterhorn_III.add_stage(M3_cone)
    Matterhorn_III.add_stage(M3_body)

    # Bla
    US_Atmos = stdAtmosUS(1382, 308, 85600, 0.15)

    # Check Rocket parameters
    print(Matterhorn_III.get_mass(3))
    print(Matterhorn_III.get_dmass_dt(3))
    print(M3_body.motors[0].thrust_to_mass)
    print(M3_body.motors[0].get_propellant_mass(3))
    print(Matterhorn_III.get_max_diameter)

    # Sim
    print(Simulator1D(Matterhorn_III, US_Atmos).xdot(0, [0, 0]))
    Simulator1D(Matterhorn_III, US_Atmos).get_integration(1001, 30)
    print(Simulator1D(Matterhorn_III, US_Atmos).xdot(1.47532025558889, [65.2079537378150,	94.4316557469021]))

    # Current simulation yields an apogee of 2031.86129 m whereas Matlab 1D yields 2022.9871 m
