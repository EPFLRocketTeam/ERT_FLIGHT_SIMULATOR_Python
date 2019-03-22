# Rocket class file
# Author : Eric Brunner
# Date   : 10 March 2019
# EPFL Rocket Team, 1015 Lausanne, Switzerland

from Rocket.Stage import Stage


class Rocket:
    """
    Rocket object
    =============

    Rocket representation class. Stores all geometrical and inertial information as well as the staging sequence.

    Attributes
    ----------

    stages : Stage[]
        an ordered list of stages constituting the rocket

    Constructor
    -----------

    __init__(*stages)
        initializes a Rocket object with the Stages included in the stage list.

    Methods
    -------

    add_stage(stage)
         Add a stage representation object to the rocket.

    """

    # ------------------
    # CONSTRUCTOR
    # ------------------

    def __init__(self, *stages: "list of Stage"):
        """
        Rocket constructor, takes an ordered list of stages constituting the rocket.
        Example: rocket = Rocket()

        :type: stages: Stage[]
        """
        self.stages = []
        self.stages.append(stages)
        self.stages.pop(0)

    # ------------------
    # METHODS
    # ------------------

    def add_stage(self, stage: Stage):
        """
        Add a stage representation object to the rocket.

        :param stage: stage representation object
        :return: None
        """
        self.stages.append(stage)

    # TODO : Add get_cg, get_length, get_inertia, get_mass, etc.

    def __str__(self):
        return self.stages.__str__()
