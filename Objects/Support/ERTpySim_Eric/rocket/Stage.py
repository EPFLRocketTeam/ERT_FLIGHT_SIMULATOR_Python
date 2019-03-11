# Rocket class file
# Author : Eric Brunner
# Date   : 10 March 2019
# EPFL Rocket Team, 1015 Lausanne, Switzerland

import numpy as np

from rocket.Fin import Fin
from rocket.Motor import Motor

class Stage:
    """
         Stage representation class. A rocket is made of many stages, each with a single body, an unlimited number of
         fins and multiple motors.

         Attributes
         ----------

        id : String
            Stage identification name, e.g. 'Upper Stage' or 'Booster Stage'

        body : Body
            reference to the body representation object of this stage

        fins : Fin[]
            list of fin representation objects

        motors : Motor[]
            list of motor representation objects

        emptyMass : float
            stage's empty mass (no motor) in kg

        emptyCG : float
            stage's CG position from the upper tip of the stage (no motor) in kg

        emptyInertia : numpy.matrix
            stage's inertia matrix (no motor) kg*m^2

        Constructor
        -----------

        __init__(id, body, emptyMass, emptyCG, emptyInertia)
            initializes a Stage object with it's name, body geometry and mass characteristics.

        Methods
        -------

        addFin(Fin)
            adds a fin representation object to the list of fins contained in this stage

        addMotor(motor)
            adds a motor representation object to the list of motors contained in this stage

         """

    # ------------------
    # CONSTRUCTOR
    # ------------------

    def __init__(self, id, body, emptyMass, emptyCG, emptyInertia):

        self.id = id
        self.body = body
        self.emptyMass = emptyMass
        self.emptyCG = emptyCG
        self.emptyInertia = emptyInertia

        self.fins = []
        self.motors = []

    # ------------------
    # METHODS
    # ------------------

    def addFin(self, finSet : Fin):
        """
        Adds a fin representation object to the stage.

        :param finSet: set of fins to be added to this stage
        :return: None
        """
        self.fins.append(finSet)

    def addMotor(self, motor: Motor):
        """
        Adds a motor representation object to the stage.

        :param motor: set of fins to be added to this stage
        :return: None
        """
        self.motors.append(motor)

    def __str__(self):
        return self.id

    def __repr__(self):
        return self.id