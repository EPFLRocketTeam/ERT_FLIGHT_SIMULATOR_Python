# Rocket class file
# Author : Eric Brunner
# Date   : 10 March 2019
# EPFL Rocket Team, 1015 Lausanne, Switzerland

class Fin:
    """
        Fin set representation object. Is limited to flat trapezoidal fins.

         Attributes
         ----------

        number : int
            number of fins per set

        rootCord : float
            fin root chord length in meters

        tipChord : float
            fin tip chord length in meters

        span : float
            fin span in meters

        sweep : float
            fin sweep in meters

        thickness : float
            fin thickness in meters

        phase : float
            fin angular phase around stage body in degrees

        bottomOffset : float
            distance between bottom of stage and bottom of fin root chord

        Constructor
        -----------

        __init__(number, rootChord, tipChord, span, sweep, thickness, phase, bottomOffset)
            initializes a Stage object with it's name, body geometry and mass characteristics.

        Methods
        -------

        getFinArea()
            returns the planar area of a fin

    """

    # ------------------
    # CONSTRUCTORS
    # ------------------

    def __init__(self,
                 number: float, root_chord: float, tip_chord: float, span: float,
                 sweep: float, thickness: float, phase: float, bottom_offset: float):
        self.number = number
        self.root_chord = root_chord
        self.tip_chord = tip_chord
        self.span = span
        self.sweep = sweep
        self.thickness = thickness
        self.phase = phase
        self.bottom_offset = bottom_offset

    # ------------------
    # METHODS
    # ------------------

    def getFinArea(self):
        """
        Computes and returns the planar area of a single fin in the set

        :return: area of a single fin in the set given in m^2
        """
        return self.span * (self.root_chord + self.tip_chord) / 2

    def __str__(self):
        return ("n : {0}, Cr : {1}, Ct : {2}, S : {3}, sw : {4}, t : {5}".format(
            self.number, self.root_chord, self.tip_chord, self.span, self.sweep, self.thickness))
