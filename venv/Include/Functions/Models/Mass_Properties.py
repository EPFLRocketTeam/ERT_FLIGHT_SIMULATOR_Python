from Rocket import Rocket
from Functions.Models.Thrust import Thrust
import numpy as np


def Mass_Properties(t: float, rocket: Rocket, Opt):

    rocket_m = rocket.get_empty_mass()
    burn_time = rocket.get_burn_time()
    propel_mass = rocket.get_propel_mass()
    motor_mass = rocket.get_motor_mass()
    thrust_to_mass = rocket.get_thrust_to_mass()


    if rocket.isHybrid == 0:
        if Opt == "Linear":
            if t == 0:
                dMdt = propel_mass/burn_time
                M = rocket_m

            elif t > burn_time:
                M = rocket_m + rocket.casing_mass
                dMdt = 0
            else:
                dMdt = propel_mass/burn_time
                M = rocket_m + motor_mass - t * dMdt
        elif Opt == "NonLinear":
            if t == 0:
                dMdt = thrust_to_mass*Thrust(t, rocket)
                M = rocket_m
            elif t > burn_time:
                M = rocket_m + motor_mass - propel_mass
                dMdt = 0
            else:
                tt = np.linspace(0, t, 500)
                current_impulse = np.trapz(tt, Thrust(tt, Rocket))
                M = rocket_m + motor_mass - thrust_to_mass * current_impulse
                dMdt = thrust_to_mass * Thrust(t, Rocket)
        else:
            print("ERROR: Opt parameter should be Linear or NonLinear")

    # Center of Mass

    Cm = (rocket.cg*rocket_m + (M-rocket_m)*(rocket.L-rocket.get_motor_length()/2))/M
    dCmdt = (dMdt * (rocket.L - rocket.get_motor_length()/2) - dMdt*Cm)/M
