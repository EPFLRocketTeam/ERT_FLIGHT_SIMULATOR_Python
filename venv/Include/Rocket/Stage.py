# Rocket class file
# Author : Eric Brunner
# Date   : 10 March 2019
# EPFL Rocket Team, 1015 Lausanne, Switzerland

from Rocket.Body import Body
from Rocket.Fins import Fins
from Rocket.Motor import Motor


class Stage:
    """
         Stage representation class. A rocket is made of many stages, each with a single body, an unlimited number of
         fins and multiple motors.

         Attributes
         ----------

        id : str
            Stage identification name, e.g. 'Upper Stage' or 'Booster Stage'.

        body : Body
            Reference to the body representation object of this stage.

        fins : Fins[]
            List of fin representation objects.

        motors : Motor[]
            List of motor representation objects.

        empty_mass : float
            Stage's empty mass (no motor) in kg.

        empty_cg : float
            Stage's CG position from the upper tip of the stage (no motor) in m.

        empty_inertia : numpy.matrix
            Stage's inertia matrix (no motor) kg.m^2.

        Constructor
        -----------

        __init__(id, body, empty_mass, empty_cg, empty_inertia)
            Initializes a Stage object with it's name, body geometry and mass characteristics.

        Methods
        -------

        add_fins(Fins)
            Adds a fin representation object to the list of fins contained in this stage.

        add_motor(motor)
            Adds a motor representation object to the list of motors contained in this stage.

         """

    # ------------------
    # CONSTRUCTOR
    # ------------------

    def __init__(self, name: str, body: Body, empty_mass: float, empty_cg: float, empty_inertia: float):
        self.name = name
        self.body = body
        self.empty_mass = empty_mass
        self.empty_cg = empty_cg
        self.empty_inertia = empty_inertia

        self.fins = []
        self.motor_paths = []
        self.motors = []

    # ------------------
    # METHODS
    # ------------------

    def add_fins(self, fin_set: Fins):
        """
        Adds a fin representation object to the stage.

        :param: fin_set: set of fins to be added to this stage
        :return: None
        """
        self.fins.append(fin_set)

    def add_motor(self, motor: Motor):
        """
        Adds a motor representation object to the stage.

        :param: motor: motor path to be added to this stage
        :return: None
        """
        self.motor_paths.append(motor)
        self.motors.append(Motor(motor))

    def get_mass(self, t: float):
        tmp_mass = 0
        if not self.fins:
            tmp_mass += sum([fin_set.total_mass for fin_set in self.fins])
        if not self.motors:
            tmp_mass += sum([motor.get_total_mass(t) for motor in self.motors])
        return self.empty_mass + tmp_mass

    def get_dmass_dt(self, t: float):
        return sum([motor.get_dmass_dt(t) for motor in self.motors])

    def get_thrust(self, t: float):
        return sum([motor.get_thrust(t) for motor in self.motors])

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
