import numpy as np
from scipy.integrate import ode

from Rocket.Body import Body
from Rocket.Fins import Fins
from Rocket.Motor import Motor
from Rocket.Rocket import Rocket
from Rocket.Stage import Stage

if __name__ == "__main__":
    """
    # Measured values
    eiger_nosecone_ogive = Body("tangent ogive", np.array([0, 0.156]), np.array([0, 0.289]), 0, 0)
    eiger_nosecone_straight = Body("cylinder", np.array([0.156, 0.156]), np.array([0, 0.307]), 0.57, 0.206)
    #
    eiger_nosecone_slide_in = Body("cylinder", np.array([0.156, 0.156]), np.array([0, 0.294]), 0.543, 0.147)
    # CATIA values
    eiger_payload = Body("cylinder", np.array([0.139, 0.139]), np.array([0, 0.2]), 4, 0.134)  # 0.242 from tip
    """

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

    print(Matterhorn_III)

    print(max(tubes_francais.diameters))
    print(Matterhorn_III.get_mass(0))

    from Functions.stdAtmosUS import stdAtmosUS

    US_Atmos = stdAtmosUS(1382, 308, 85600, 0.15)

    from Functions.drag import drag

    t = 6.11840823842032
    x = [853.848962337705, 166.003984138695]
    T = Matterhorn_III.get_thrust(t)
    M = Matterhorn_III.get_mass(t)
    dMdt = Matterhorn_III.get_dmass_dt(t)
    rho = US_Atmos.get_density(x[0] + US_Atmos.ground_altitude)
    nu = US_Atmos.get_viscosity(x[0] + US_Atmos.ground_altitude)
    a = US_Atmos.get_speed_of_sound(x[0] + US_Atmos.ground_altitude)
    # TODO: Add drag influences (done?)
    CD = drag(Matterhorn_III, 0, x[1], nu, a)
    print('t = ', t)
    print('x = ', x)
    print('Thrust = ', T)
    print('Rocket mass = ', M)
    print('dMdt = ', dMdt)
    print('Air density = ', rho)
    print('Air viscosity = ', nu)
    print('Speed of sound = ', a)
    print('CD = ', CD)

    from scipy.integrate import solve_ivp
    import matplotlib.pyplot as plt


    def xdot(t, x):
        dir = -1
        return [dir * mu * (x[0] - 1 / 3 * x[0] ** 3 - x[1]), dir * 1 / mu * x[0]]


    x_0 = [-2, 0]
    t0 = 0
    max_time = 10000

    nTps = [101, 1001, 10001, 100001]
    fig = plt.figure(figsize=(6, 4))
    for i in range(4):
        ntps = nTps[i]
        tspan = np.linspace(max_time, t0, ntps)
        plt.subplot(2, 2, i+1)

        for mu in [1, 2, 3, 4, 5]:
            integration_ivp = solve_ivp(xdot, [max_time, t0], x_0, method='RK45')

            print('mu = ')
            print(mu)

            plt.plot(integration_ivp.y[0], integration_ivp.y[1])
        plt.title("".join(['t0 = ', str(max_time), ', tf = ', str(t0), ', n = ', str(ntps)]))
    plt.show()
