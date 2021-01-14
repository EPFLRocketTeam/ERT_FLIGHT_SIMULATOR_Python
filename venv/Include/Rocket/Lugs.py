# Rocket class file
# Author : Sayid Derder
# Date   : 07.12.2020
# EPFL Rocket Team, 1015 Lausanne, Switzerland


class Lugs:
    """
    lug_n: int

    lug_S: float

    """

    def __init__(self, lug_n: int, lug_S: float):

        self.lug_n = lug_n
        self.lug_S = lug_S

    @property
    def get_lug_n(self):
        return self.lug_n

    @property
    def get_lug_S(self):
        return self.lug_S


