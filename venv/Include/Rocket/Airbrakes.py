# Rocket class file
# Author : Sayid Derder
# Date   : 07.12.2020
# EPFL Rocket Team, 1015 Lausanne, Switzerland


class Airbrakes:
    """
    ab_x: float

    ab_n: int

    ab_phi: float

    """

    def __init__(self, ab_x: int, ab_n: int, ab_phi: float):

        self.ab_x = ab_x
        self.ab_n = ab_n
        self.ab_phi = ab_phi

    @property
    def get_ab_n(self):
        return self.ab_n

    @property
    def get_ab_x(self):
        return self.ab_x

    @property
    def get_ab_phi(self):
        return self.ab_phi


