import numpy as np

from Rocket.Body import Body
from Rocket.Rocket import Rocket
from Rocket.Stage import Stage

if __name__ == "__main__":
    gland = Body("tangent ogive", np.array([0, 0.123]), np.array([0, 0.428]))

    tubes_francais = Body("cylinder", np.array([0.123, 0.123, 0.103]), np.array([0, 1.815, 1.863]))

    M3_cone = Stage('Matterhorn III nosecone', gland, 1.5, 0.338, np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]]))

    M3_body = Stage('Matterhorn III body', tubes_francais, 9.9, 0.930, np.array([[2.72, 0, 0], [0, 2.72, 0], [0, 0, 0]]))

    finDefData = {'number': 3,
                  'root_chord': 0.24,
                  'tip_chord': 0.12,
                  'span': 0.11,
                  'sweep': 0.06,
                  'thickness': 0.003,
                  'phase': 0,
                  'bottom_offset': 0}

    M3_body.add_fins(finDefData)

    M3_body.add_motor('Motor/Cesaroni_M1800.eng')

    Matterhorn_III = Rocket()

    Matterhorn_III.add_stage(M3_cone)
    Matterhorn_III.add_stage(M3_body)

    print(Matterhorn_III)
