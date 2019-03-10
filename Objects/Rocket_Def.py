from scipy.interpolate import interp1d
from scipy.integrate import simps
import numpy as np
import bisect

class Rocket:

    def inertia(self):
        pass

    pass

class Stage:

    EMPTY_MASS = 0
    EMPTY_CG = 0
    EMPTY_INERTIA = 0

    def inertia(self):
        pass

class Body:

    CONE_TYPE = 0
    DIAMETERS = []
    DIAMETERS_POS = []

class Fins:

    NUMBER = 0
    ROOT_CORD = 0
    TIP_CORD = 0
    SPAN = 0
    SWEEP = 0
    BASE_POS = 0

    @property
    def area(self):
        pass

class Motor:

    def __init__(self,motor_file_path):
        with open(motor_file_path,"r") as motor_data:
            motor_data.readline()
            general_data = motor_data.readline.split()

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
            self.thrust_time = [0, self.thrust_time]
            self.thrust_force = [0, self.thrust_force]

        # Linear interpolation of the thrust force samples
        self.thrust_function = interp1d(self.thrust_time,self.thrust_force)

        self.burn_time = self.thrust_time[-1]

        # Simpson integration of the thrust curve
        sample_time = np.linspace(0, self.burn_time, num=2000)
        sample_thrust = self.thrust_function(sample_time)
        self.total_impulse = simps(sample_thrust, sample_time, even='avg')

        self.thrust_to_mass = self.propellant_mass / self.total_impulse


    
    def get_thrust(self, t):
        if(0 <= t <= self.burn_time):
            return self.thrust_function(t)
        else:
            return 0

    def get_mass(self, t):
        thrust_t = self.thrust_time[:bisect.bisect_right(self.thrust_time, t)]
        thrust_f = self.thrust_force[:bisect.bisect_right(self.thrust_force, t)]
        current_impulse = simps(thrust_f, thrust_t, even='avg')
        return self.total_mass - self.thrust_to_mass * current_impulse

    def get_CG(self):
        pass
    
    def get_inertia(self):
        pass

def main():
    pass

if __name__ == "__main__":
    main()