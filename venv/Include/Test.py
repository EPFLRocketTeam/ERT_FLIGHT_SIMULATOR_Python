import numpy as np
import math
from scipy.integrate import ode

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

    # Rocket definition
    gland = Body('tangent ogive', [0, VAL_N[1] * 10 ** (-3)], [0, (VAL_N[0]) * 10 ** (-3)])

    tubes_francais = Body("cylinder", [VAL_N[1] * 10 ** (-3), VAL_BT[1] * 10 ** (-3), VAL_BT[2] * 10 ** (-3)],
                          [0, (VAL_T[0] + VAL_F[9]) * 10 ** (-3), (VAL_T[0] + VAL_F[9] + VAL_BT[0]) * 10 ** (-3)])

    # TODO: Add Mass and CM to stage
    M3_cone = Stage('Matterhorn III nosecone', gland, 1.26, 0.338, np.array([[VAL_N[2], VAL_N[3], VAL_N[4]],
                                                                             [VAL_N[5], VAL_N[6], VAL_N[7]],
                                                                             [VAL_N[8], VAL_N[9], VAL_N[10]]]))
    M3_body = Stage('Matterhorn III body', tubes_francais, 9.6, 0.930, np.array([[VAL_T[2], VAL_T[3], VAL_T[4]],
                                                                                 [VAL_T[5], VAL_T[6], VAL_T[7]],
                                                                                 [VAL_T[8], VAL_T[9], VAL_T[10]]]))
    finDefData = {'number': VAL_F[0],
                  'root_chord': VAL_F[1] * 10 ** (-3),
                  'tip_chord': VAL_F[2] * 10 ** (-3),
                  'span': VAL_F[3] * 10 ** (-3),
                  'sweep': VAL_F[4] * 10 ** (-3),
                  'thickness': VAL_F[5] * 10 ** (-3),
                  'phase': VAL_F[6],
                  'body_top_offset': (VAL_T[0] + VAL_F[7]) * 10 ** (-3),
                  'total_mass': VAL_F[8] * 10 ** (-3)}

    M3_body.add_fins(finDefData)

    M3_body.add_motor('Motors/%s.eng' % (Motor1[0]))

    Matterhorn_III = Rocket()

    Matterhorn_III.add_stage(M3_cone)
    Matterhorn_III.add_stage(M3_body)

    print(len(Matterhorn_III.stages))
    print(Matterhorn_III.diameters_position)
    print(Matterhorn_III.diameters)

    # (a, b) = robert_galejs_lift(Matterhorn_III, 0.8, 270)
    # print(a, b)
