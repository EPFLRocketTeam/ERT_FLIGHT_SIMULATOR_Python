# Author : Michaël Tasev
# Last update : 16 October 2020
# EPFL Rocket Team, 1015 Lausanne, Switzerland

import numpy as np
from scipy import interpolate


def wind_model(t, I, V_inf, Model, h_alt):
    t_wind_ = []
    wind_ = []

    if Model == 'None':
        U = V_inf

    else:
        if not t_wind_:
            t_wind_ = 0
            wind_ = V_inf

        if Model == 'Gaussian':  # TODO : add VonKarman model (needs to be complete on MatLab too) and Logarithmic model
            if t > t_wind_[-1]:
                t_wind_.append(t)
                turb_std = I * V_inf
                U = np.random.normal(V_inf, turb_std)
                wind_.append(U)
            else:
                U = interpolate.interp1d(t_wind_, wind_.transpose(), t, 'linear')
        else:
            raise Exception("wind_model ", Model, " is unknowkn")

    return U
