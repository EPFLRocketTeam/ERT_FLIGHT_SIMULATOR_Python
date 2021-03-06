# Author : Henri Faure
# Date : 31 March 2019
# EPFL Rocket Team, 1015 Lausanne, Switzerland

def drag_shuriken(Rocket, theta, alpha, Uinf, nu):
# DRAG_SHURIKEN estimates the drag coefficient normalized to the Rocket's
# reference area for the shuriken airbrake design.
# INPUTS : 
# - Rocket  : Rocket object
# - theta   : Airbrakes command input, -190.5 = closed, 1.165 = open [deg]
# - alpha   : wind angle of attack [rad]
# - Uinf    : Air free stream velocity [m/s]
# - nu      : dynamic viscosity coefficient [m2/s]

    import numpy as np
    import math
    from scipy.interpolate import interp1d

    # parameters
    theta_tab = [-190.5, -171.330000000000, -152.167000000000, -133, -113.834000000000, -94.6675000000000,
                 -75.5010000000000, -56.3345000000000, -37.1680000000000, -18.0015000000000, 1.16500000000000]
    h_tab = [0, 4.34907316225958, 8.43601280366038, 12.5714441240868, 15.9617850714579, 19.4274461716749,
             22.5198715099807, 25.1590682806241, 27.3885534922061, 29.0649328894631, 30.2695855614939]*1e-3
    l_tab = [41, 41.2875998204350, 41.8992465244594, 42.8866122807265, 42.8847802958924, 43.7175646267330,
             44.4172346752755, 44.8118095534585, 45.9093561387191, 46.8032591379062, 47.4986783215347]*1e-3
    CD0 = 1.17
    U = abs(Uinf*math.cos(alpha))
    Rex = Rocket.ab_x*U/nu
    delta = 0.37*Rocket.ab_x/Rex**0.2
    
    # interpolate data
    h = interp1d(theta_tab, h_tab)(theta)
    l = interp1d(theta_tab, l_tab)(theta)
    
    # compute values
    # surface
    S = 0.5*h*l
    # drag coefficient
    if h < delta:
        qr = 49/72*(h/delta)**(2/7)
    else:
        qr = 1 - 4/9*delta/h+1/8*(delta/h)**2

    CD = Rocket.ab_n*CD0*qr*S/Rocket.get_max_cross_section_surface

    return CD
