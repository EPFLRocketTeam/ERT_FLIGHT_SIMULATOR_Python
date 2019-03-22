# Rocket class file
# Author : Eric Brunner
# Date   : 10 March 2019
# EPFL Rocket Team, 1015 Lausanne, Switzerland


class Fins:
    """
    Fins object
    ===========

    Fin set representation object. It is limited to flat trapezoidal fins.

     Attributes
     ----------

    number : int
        Number of fins per set.

    root_chord : float
        Fin root chord length in m.

    tip_chord : float
        Fin tip chord length in m.

    span : float
        Fin span in m.

    sweep : float
        Fin sweep in m.

    thickness : float
        Fin thickness in m.

    phase : float
        Fin angular phase around stage body in degrees.

    bottom_offset : float
        Distance between bottom of stage and bottom of fin root chord.

    Constructor
    -----------

    __init__(number, root_chord, ti_chord, span, sweep, thickness, phase, bottom_offset)
        Initializes a Stage object with it's name, body geometry and mass characteristics.

    Methods
    -------

    get_fin_area()
        returns the planar area of a fin

    """

    # --------------------
    # CONSTRUCTORS
    # --------------------

    def __init__(self,
                 number: int, root_chord: float, tip_chord: float, span: float,
                 sweep: float, thickness: float, phase: float, bottom_offset: float):
        self.number = number
        self.root_chord = root_chord
        self.tip_chord = tip_chord
        self.span = span
        self.sweep = sweep
        self.thickness = thickness
        self.phase = phase
        self.bottom_offset = bottom_offset

    # --------------------
    # METHODS
    # --------------------

    @property
    def get_fin_area(self):
        """
        Computes and returns the planar area of a single fin in the set.

        :return: area of a single fin in the set given in m^2
        """
        return self.span * (self.root_chord + self.tip_chord) / 2
