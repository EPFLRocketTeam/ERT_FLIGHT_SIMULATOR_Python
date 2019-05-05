# Rocket class file
# Author : Jules Triomphe
# Date   : 5 May 2019
# EPFL Rocket Team, 1015 Lausanne, Switzerland

from Rocket.Stage import Stage
from scipy.interpolate import interp1d
import numpy as np


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
        Initializes a Rocket object with the Stages included in the stage list.

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
        if np.any(stages):
            self.stages = [stage for stage in stages]
            print(self.stages)

        self.diameters = []
        if np.any(stages):
            self.diameters = [diameter for diameter in [stage.body.diameters for stage in self.stages]]

        self.diameters_position = []
        if np.any(stages):
            self.diameters_position = [stage.body.diameters_position for stage in self.stages]

        # TODO: Implement or modify the expression of these parameters
        self.cone_mode = 'on'
        self.ab_n = 3 # TODO: Create an airbrake section in Body or find another way to implement them
        self.ab_x = 1.390
        self.lug_n = 2
        self.lug_S = 1.32e-4
        # Arbitrary, based on M3 launch lugs in Cernier 23/03/2019; 1.61e-4 for M2
        # TODO: Implement this parameter in the definition of the body and then for the rocket as a whole


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

        if np.any(self.diameters):
            self.diameters.extend(stage.body.diameters)
        else:
            self.diameters = stage.body.diameters

        if np.any(self.diameters_position):
            corrected_diameter_position = [diameter_position + self.diameters_position[-1] for
                                           diameter_position in stage.body.diameters_position]
            self.diameters_position.extend(corrected_diameter_position)
        else:
            self.diameters_position = stage.body.diameters_position

    def get_cg(self):
        pass

    # TODO : Add get_cg, get_inertia, etc.

    @property
    def get_length(self):
        return max(self.diameters_position)

    def get_mass(self, t: float):
        return sum([stage.get_mass(t) for stage in self.stages])

    def get_dmass_dt(self, t: float):
        return sum([stage.get_dmass_dt(t) for stage in self.stages])

    def get_thrust(self, t: float):
        return sum([stage.get_thrust(t) for stage in self.stages])

    @property
    def get_max_diameter(self):
        return max([stage.body.max_diameter for stage in self.stages])

    @property
    def get_max_cross_section_surface(self):
        return max([stage.body.max_cross_section_surface for stage in self.stages])

    @property
    def get_fin_chord(self):
        for stage in self.stages:
            if stage.fins:
                return (stage.fins[0].root_chord + stage.fins[0].tip_chord) / 2
            # TODO: Implement a way to have the fin chord for each fin set. Modify drag function in accordance.

    @property
    def get_fin_span(self):
        for stage in self.stages:
            if stage.fins:
                return stage.fins[0].span

    @property
    def get_fin_exposed_planform_area(self):
        for stage in self.stages:
            if stage.fins:
                return (stage.fins[0].root_chord + stage.fins[0].tip_chord) / 2 * stage.fins[0].span

    @property
    def get_mid_fin_diameter(self):
        for stage in self.stages:
            if stage.fins:
                diameter_at_position_function = interp1d(stage.body.diameters_position, stage.body.diameters)
                return diameter_at_position_function(stage.fins[0].body_top_offset + stage.fins[0].root_chord / 2)
            # TODO: Find a way to organize this when multiple fin sets per body are involved or when the diameter...
            #  is changing and fins are offsetted (e.g. Hydra)

    @property
    def get_fin_virtual_planform_area(self):
        for stage in self.stages:
            if stage.fins:
                return self.get_fin_exposed_planform_area + 0.5 * self.get_mid_fin_diameter * stage.fins[0].root_chord

    @property
    def get_fin_thickness(self):
        for stage in self.stages:
            if stage.fins:
                return stage.fins[0].thickness

    @property
    def get_fin_number(self):
        for stage in self.stages:
            if stage.fins:
                return stage.fins[0].number

    def __str__(self):
        return self.stages.__str__()
