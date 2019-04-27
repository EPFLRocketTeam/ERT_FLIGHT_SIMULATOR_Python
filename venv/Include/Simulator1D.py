# Motor class file
# Author : Jules Triomphe
# Date : 23 March 2019
# EPFL Rocket Team, 1015 Lausanne, Switzerland

import numpy as np
from scipy.integrate import ode

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
        self.t0, self.t1 = 0, 28

        self.Rocket = rocket
        self.time_span = np.linspace(self.t0, self.t1, 100)
        self.Atmosphere = atmosphere

    def xdot(self, t, x):
        T = self.Rocket.get_thrust(t)
        M = self.Rocket.get_mass(t)
        dMdt = self.Rocket.get_dmass_dt(t)
        rho = self.Atmosphere.get_density(t)
        nu = self.Atmosphere.get_viscosity(x[0] + US_Atmos.ground_altitude + 5)
        a = self.Atmosphere.get_speed_of_sound(x[0] + US_Atmos.ground_altitude + 5)
        # TODO: Add drag influences
        CD = drag(self.Rocket, 0, x[1], nu, a)
        CD_AB = 0  # TODO: Insert reference to drag_shuriken or other
        g = self.Atmosphere.G0
        d = self.Rocket.get_d_max
        return [x[1], T / M - g - x[1] * dMdt / M - 0.5 * rho * d * x[1] ** 2 * (CD + CD_AB) / M]

    def get_integration(self):
        integration = ode(self.xdot).set_integrator('dopri5').set_initial_value(self.x_0, self.t0)
        while integration.successful(): # and integration.y[1] > 0:
            print(1)
            print(integration.t+0.01, integration.integrate(integration.t+0.01))
        return


if __name__ == '__main__':
    # Rocket definition
    gland = Body("tangent ogive", [0, 0.123], [0, 0.428])

    tubes_francais = Body("cylinder", [0.123, 0.123, 0.103], [0, 1.815, 1.863])

    M3_cone = Stage('Matterhorn III nosecone', gland, 1.5, 0.338, np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]]))

    M3_body = Stage('Matterhorn III body', tubes_francais, 9.9, 0.930,
                    np.array([[2.72, 0, 0], [0, 2.72, 0], [0, 0, 0]]))

    finDefData = {'number': 3,
                  'root_chord': 0.236,
                  'tip_chord': 0.118,
                  'span': 0.128,
                  'sweep': 0.06,
                  'thickness': 0.003,
                  'phase': 0,
                  'body_top_offset': 1.54}

    M3_body.add_fins(finDefData)

    M3_body.add_motor('Motors/Cesaroni_M1800.eng')

    Matterhorn_III = Rocket()

    Matterhorn_III.add_stage(M3_cone)
    Matterhorn_III.add_stage(M3_body)

    # Bla
    US_Atmos = stdAtmosUS(1382, 308, 86000, 0.15)

    # Check Rocket parameters
    print(Matterhorn_III.get_mass(0))

    print(Matterhorn_III.get_max_diameter)

    # Sim
    Simulator1D(Matterhorn_III, US_Atmos).xdot(0, [0, 0])
    Simulator1D(Matterhorn_III, US_Atmos).get_integration()
