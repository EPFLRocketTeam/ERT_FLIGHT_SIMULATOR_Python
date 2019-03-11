# Rocket class file
# Author : Eric Brunner
# Date   : 10 March 2019
# EPFL Rocket Team, 1015 Lausanne, Switzerland

from rocket.Stage import Stage

class Rocket:
    """
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

    addStage(stage)
         Add a stage representation object to the rocket.

    """

    # ------------------
    # CONSTRUCTOR
    # ------------------

    def __init__(self, *stages: "list of Stage"):
        """
        Rocket constructor, takes an ordered list of stages constituting the rocket.
        Example: rocket = Rocket()

        :type stages: Stage[]
        """
        self.stages = stages

    # ------------------
    # METHODS
    # ------------------

    def addStage(self, stage : Stage ):
        """
        Add a stage representation object to the rocket.

        :param stage: stage representation object
        :return: None
        """
        self.stages.append(stage)

    def __str__(self):
        return self.stages.__str__()

