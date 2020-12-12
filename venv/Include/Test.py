import numpy as np
import math
from scipy.integrate import ode
import matplotlib.pyplot as plt

from Rocket.Body import Body
from Rocket.Fins import Fins
from Rocket.Motor import Motor
from Rocket.Rocket import Rocket
from Rocket.Stage import Stage
from Functions import Math
from Functions.Math.quat2rotmat import quat2rotmat
from Functions.Math.rot2anglemat import rot2anglemat
from Functions.Math.normalize_vector import normalize_vector
from Functions.Math.quat_evolve import quat_evolve
from Functions.Models.wind_model import wind_model
from Functions.Models.robert_galejs_lift import robert_galejs_lift
from Functions.Models.barrowman_lift import barrowman_lift
from Functions.Math.rot2quat import rot2quat
from Functions.Models.stdAtmosUS import stdAtmosUS
from Simulator3D import Simulator3D

if __name__ == "__main__":

    NoseCone = open('Parameters/param_rocket/NoseCone.txt', 'r')  # Read text file
    NoseCone1 = NoseCone.readlines()
    VAL_N = []
    for line in NoseCone1:  # taking each line
        conv_float = float(line)
        VAL_N.append(conv_float)

    Tube = open('Parameters/param_rocket/Tube.txt', 'r')
    Tube1 = Tube.readlines()
    VAL_T = []
    for line in Tube1:  # taking each line
        conv_float = float(line)
        VAL_T.append(conv_float)

    Fins = open('Parameters/param_rocket/Fins.txt', 'r')
    Fins1 = Fins.readlines()
    VAL_F = []
    for i, line in enumerate(Fins1):  # taking each line
        if i == 0:
            conv_int = int(float(line))
            VAL_F.append(conv_int)
        else:
            conv_float = float(line)
            VAL_F.append(conv_float)

    BoatTail = open('Parameters/param_rocket/BoatTail.txt', 'r')
    BoatTail1 = BoatTail.readlines()
    VAL_BT = []
    for line in BoatTail1:  # taking each line
        conv_float = float(line)
        VAL_BT.append(conv_float)

    Motor = open('Parameters/param_motor/Motor.txt', 'r')
    Motor1 = Motor.readlines()

    Env = open('Parameters/param_env/Env.txt', 'r')
    Env1 = Env.readlines()
    VAL_E = []
    for line in Env1:  # taking each line
        conv_float = float(line)
        VAL_E.append(conv_float)

    Lugs = open('Parameters/param_rocket/LugsTube.txt', 'r')
    Lugs1 = Lugs.readlines()
    VAL_L = []
    for line in Lugs1:  # taking each line
        conv_float = float(line)
        VAL_L.append(conv_float)

    AB = open('Parameters/param_rocket/AirBrakesTube.txt', 'r')
    AB1 = AB.readlines()
    VAL_AB = []
    for line in AB1:  # taking each line
        conv_float = float(line)
        VAL_AB.append(conv_float)

    weight = open('Parameters/param_rocket/WeightTube.txt', 'r')
    weight1 = weight.readlines()
    VAL_W = []
    for line in weight1:  # taking each line
        conv_float = float(line)
        VAL_W.append(conv_float)

    MP = open('Parameters/param_rocket/ParachuteTubeMain.txt', 'r')
    MP1 = MP.readlines()
    VAL_MP = []
    for line in MP1:  # taking each line
        conv_float = float(line)
        VAL_MP.append(conv_float)

    DP = open('Parameters/param_rocket/ParachuteTubeDrogue.txt', 'r')
    DP1 = DP.readlines()
    VAL_DP = []
    for line in DP1:  # taking each line
        conv_float = float(line)
        VAL_DP.append(conv_float)

    weight = open('Parameters/param_rocket/WeightTube.txt', 'r')
    weight1 = weight.readlines()
    VAL_W = []
    for line in weight1:  # taking each line
        conv_float = float(line)
        VAL_W.append(conv_float)

    # Rocket definition
    gland = Body('tangent ogive', [0, 0.156], [0, 0.242])

    tubes_francais = Body("cylinder", [0.156, 0.135],
                          [4.11-0.242, 4.16-0.242])

    # TODO: Add Mass and CM to stage
    M3_cone = Stage('Matterhorn III nosecone', gland, 5, 0.338, np.array([[VAL_N[2], VAL_N[3], VAL_N[4]],
                                                                             [VAL_N[5], VAL_N[6], VAL_N[7]],
                                                                             [VAL_N[8], VAL_N[9], VAL_N[10]]]))
    M3_body = Stage('Matterhorn III body', tubes_francais, 29.3, 0.930, np.array([[VAL_T[2], VAL_T[3], VAL_T[4]],
                                                                                 [VAL_T[5], VAL_T[6], VAL_T[7]],
                                                                                 [VAL_T[8], VAL_T[9], VAL_T[10]]])) # TODO: Change empty mass and empty CG mass without fins
    finDefData = {'number': 3,
                  'root_chord': 0.28,
                  'tip_chord': 0.125,
                  'span': 0.2,
                  'sweep': 0.107,
                  'thickness':  0.004,
                  'phase': VAL_F[6],
                  'body_top_offset': 3.83,
                  'total_mass': 0.5}

    M3_body.add_fins(finDefData)
    M3_body.add_motor('Motors/%s.eng' % (Motor1[0]))

    main_parachute_params = [bool(VAL_MP[4]), VAL_MP[5], VAL_MP[5]]
    M3_body.add_parachute(main_parachute_params)

    drogue_parachute_params = [bool(VAL_DP[4]), VAL_DP[5], VAL_DP[5]]
    M3_body.add_parachute(drogue_parachute_params)

    ab_data = [VAL_T[0]/2 + VAL_AB[4], 0, VAL_AB[3]]
    M3_body.add_airbrakes(ab_data)

    Matterhorn_III = Rocket()

    Matterhorn_III.add_stage(M3_cone)
    Matterhorn_III.add_stage(M3_body)
    Matterhorn_III.add_lugs([VAL_L[2], 5.7*10**(-4)]) # TODO: Add lug surface

    Matterhorn_III.set_payload_mass(VAL_W[0])
    Matterhorn_III.add_cg_empty_rocket(2.14)
    Matterhorn_III.set_rocket_inertia(47)

    US_Atmos = stdAtmosUS(1567, 290.15, 84972.484, 0.51031)

    SimObj = Simulator3D(Matterhorn_III, US_Atmos)

    # -----------------------------------
    # Rail Sim
    # -----------------------------------

    T1, S1 = SimObj.RailSim()
    print("Launch rail departure velocity: ", S1[1][-1])
    print("Launch rail departure time: ", T1[-1])

    # -----------------------------------
    # Flight Sim
    # -----------------------------------

    T2_1, S2_1, T2_1E, S2_1E, I2_1E = SimObj.FlightSim([T1[-1], SimObj.rocket.get_burn_time()], S1[1][-1])
    T2_2, S2_2, T2_2E, S2_2E, I2_2E = SimObj.FlightSim([T2_1[-1], 40], [S2_1[i][-1] for i in range(3)], [S2_1[i][-1] for i in range(3,6)], [S2_1[i][-1] for i in range(6,10)], [S2_1[i][-1] for i in range(10,13)])

    plt.plot(T2_2, S2_2[2])
    plt.xlabel("Time [s]");
    plt.ylabel("Altitude [m]")
    plt.title("Position(time), on rail")
    plt.show()

    T2 = np.concatenate([T2_1, T2_2[1:]])
    S2 = []
    for i, s in enumerate(S2_2):
        S2.append(np.concatenate([S2_1[i], s[1:]]))

    T_1_2 = np.concatenate([T1, T2])
    # TODO : S1 ..........................


