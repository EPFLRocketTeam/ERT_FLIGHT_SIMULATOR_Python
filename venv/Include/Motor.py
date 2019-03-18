# Motor class file
# Author : Jules Triomphe
# Date : 15 March 2019
# EPFL Rocket Team, 1015 Lausanne, Switzerland

from scipy.interpolate import interp1d
from scipy.integrate import simps
import numpy as np
import bisect


class Motor:
    """

        Motor object

        ==========


        Attributes
        ----------

        diameter : float
            Motor diameter (with casing) in meters.

        length : float
            Motor length (with casing) in meters.

        delay_type : str
            Time after burnout when the ejection charge ignites.
            Classifications :
                - Number : Time in seconds
                - T : Tiny
                - M : Medium (~10 s)
                - P : Plugged ; no ejection charge
                - N/A or not listed : not adjustable

        propellant_mass : float
            Propellant mass in kg.
            Value is constant.
            To get the actual mass of the motor, use the get_mass() method.

        total_mass : float
            Total mass in kg.

        casing_mass : float
            Casing mass in kg.
            Value is constant.
            Equal to the difference between the total mass and the propellant mass.

        thrust_pairs : list of str
            Table of the sampled thrust at the corresponding time after ignition.

        thrust_time : list of float
            First column of thrust_pairs listing the time of the provided thrust samples.
            A 0 value is added at the beginning to provide a range from ignition to burnout.

        thrust_force : list of float
            Second column of thrust_pairs listing the thrust at the provided sampling times.
            A 0 value is added at the beginning to provide a data set from ignition to burnout.

        thrust_function : interp1d function
            Handle to calculate the thrust at a given time t between ignition at t=0 and burnout at t=burn_time.
            Should be used as thrust_function(t).

        burn_time : float
            Motor burn time given by the last sampling time of the motor data sheet.

        total_impulse : float64
            Total impulse of the motor given by a Simpson interpolation of the samples.

        thrust_to_mass : float64
            Thrust to mass ratio of the motor.
            Used to calculate the mass during burn.


        Constructor
        ----------

        __init__(motor_file_path)
            Initializes a motor with its physical and mathematical characteristics from a given motor data sheet path.
            The motor file can be a .txt or a .eng file.


        Methods
        ----------

        get_thrust(t)
            Returns the thrust of the motor at time t.

        get_mass(t)
            Returns the mass of the motor at time t.

        get_cg()
            Returns the center of mass of the motor.
            TODO : Rethink the output of the method.

        get_inertia()
            Returns the inertia tensors of the motor.
            TODO : Review the output/description of the method.

    """

    # --------------------
    # CONSTRUCTOR
    # --------------------

    def __init__(self, motor_file_path: str):
        with open(motor_file_path, "r") as motor_data:
            motor_data.readline()
            general_data = motor_data.readline().split()

            self.diameter = float(general_data[1]) / 1000
            self.length = float(general_data[2]) / 1000
            self.delay_type = general_data[3]

            self.propellant_mass = float(general_data[4])
            self.total_mass = float(general_data[5])
            self.casing_mass = self.total_mass - self.propellant_mass

            # First value is thrust time
            # Second value is thrust force
            self.thrust_pairs = [line.split() for line in motor_data]
            self.thrust_time = [float(thrust[0]) for thrust in self.thrust_pairs]
            self.thrust_force = [float(thrust[1]) for thrust in self.thrust_pairs]
            # Correct to add (0,0) point
            self.thrust_time.insert(0, 0)
            self.thrust_force.insert(0, 0)

        # Linear interpolation of the thrust force samples
        self.thrust_function = interp1d(self.thrust_time, self.thrust_force)

        self.burn_time = self.thrust_time[-1]

        # Simpson integration of the thrust curve
        sample_time = np.linspace(0, self.burn_time, num=2000)
        sample_thrust = self.thrust_function(sample_time)
        self.total_impulse = simps(sample_thrust, sample_time, even='avg')

        self.thrust_to_mass = self.propellant_mass / self.total_impulse

    # --------------------
    # METHODS
    # --------------------

    def get_thrust(self, t: float):
        if 0 <= t <= self.burn_time:
            return self.thrust_function(t)
        else:
            return 0

    def get_mass(self, t: float):
        if t >= 0:
            thrust_t = self.thrust_time[:bisect.bisect_right(self.thrust_time, t)]
            thrust_f = self.thrust_force[:len(thrust_t)]
            current_impulse = simps(thrust_f, thrust_t, even='avg')
            return self.total_mass - self.thrust_to_mass * current_impulse
        else:
            return self.total_mass

    @property
    def get_cg(self):
        return self.length / 2

    def get_inertia(self):
        # TODO : Find inertia model and implement it
        pass


if __name__ == '__main__':
    # Location of current motor test file
    CS_M1800 = Motor('Motors/Cesaroni_M1800.eng')
    # get_thrust method test
    print(CS_M1800.get_thrust(5))
    # get_mass method tests
    print(CS_M1800.get_mass(-3))
    print(CS_M1800.get_mass(10))