import numpy as np

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

    gland = Body("tangent ogive", np.array([0, 0.123]), np.array([0, 0.428]))

    tubes_francais = Body("cylinder", np.array([0.123, 0.123, 0.103]), np.array([0, 1.815, 1.863]))

    M3_cone = Stage('Matterhorn III nosecone', gland, 1.5, 0.338, np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]]))

    M3_body = Stage('Matterhorn III body', tubes_francais, 9.9, 0.930, np.array([[2.72, 0, 0], [0, 2.72, 0], [0, 0, 0]]))

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

    print(Matterhorn_III)

    """stage1 = Stage('Stage1', boy1, 10, 1.05, np.array([[8, 0, 0], [0, 8, 0], [0, 0, 0]]))

    finDefData = {'number': 3,
                  'root_chord': 0.28,
                  'tip_chord': 0.125,
                  'span': 0.2,
                  'sweep': 0.107,
                  'thickness': 0.003,
                  'phase': 0,
                  'bottom_offset': 0}

    stage1.add_fins(Fins(**finDefData))

    M1800 = Motor('Motors/Cesaroni_M1800.eng')

    stage1.add_motor(M1800)

    stages = [stage1]

    Rocket1 = Rocket(stages)

    print(isinstance(Rocket1, Rocket))
    print(Rocket1)
    print(stage1)"""

    print(max(tubes_francais.diameters))