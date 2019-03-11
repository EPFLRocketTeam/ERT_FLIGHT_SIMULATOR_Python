import numpy as np

from rocket.Rocket import Rocket
from rocket.Fin import Fin
from rocket.Motor import Motor
from rocket.Stage import Stage
from rocket.Body import Body

if __name__ == '__main__':

    stage1 = Stage('Stage1', Body(), 10, 1.05, np.matrix([[8, 0, 0],
                                                     [0, 8, 0],
                                                     [0, 0, 0]]))
    finDefData = {'number': 3,
                  'rootChord': 0.15,
                  'tipChord': 0.1,
                  'span': 0.11,
                  'sweep': 0.025,
                  'thickness': 0.003,
                  'phase': 0,
                  'bottomOffset': 0}

    stage1.addFin(Fin(**finDefData))

    stage2 = Stage('Stage2', Body(), 7, 0.8, np.matrix([[4, 0, 0],
                                               [0, 4, 0],
                                               [0, 0, 0]]))

    finDefData = {'number': 3,
                  'rootChord': 0.2,
                  'tipChord': 0.13,
                  'span': 0.15,
                  'sweep': 0.03,
                  'thickness': 0.003,
                  'phase': 0,
                  'bottomOffset': 0}

    stage2.addFin(Fin(**finDefData))

    stages = [
        stage1,
        stage2
    ]

    rocket = Rocket(*stages)

    print(rocket)

    for stage in stages:
        print(stage)
        for fin in stage.fins:
            print("    {0}".format(fin))