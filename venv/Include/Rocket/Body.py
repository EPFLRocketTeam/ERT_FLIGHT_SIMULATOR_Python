# Body class file
# Author : Jules Triomphe
# Date : 22 March 2019
# EPFL Rocket Team, 1015 Lausanne, Switzerland


class Body:
    """
        Body object
        ==========


        Attributes
        ----------

        cone_type : str
            "cylinder","tangent ogive"
            TODO : Implement "conic", "spherically blunted conic", "bi-conic", "spherically blunted tangent ogive",
                "secant ogive", "elliptical", "parabola", "3/4 parabola", "1/2 parabola", "1/2 power", "3/4 power",
                "LV-Haack", "Von Karman" or "LD-Haack", "tangent Haack", "aerospike"

        diameters : list of float
            Diameters at beginning and end of section changes.
            Diameters in m.

        diameters_pos : list of float
            Position of the self.diameters in m.
            Measured from the top of the body.

    """

    # --------------------
    # CONSTRUCTOR
    # --------------------

    def __init__(self, cone_type: str, diameters: "np array", diameters_pos: "np array"):
        self.cone_type = cone_type
        self.diameters = diameters
        self.diameters_pos = diameters_pos
