from creation_of_test_data.generate_random_parameters import get_random_parameters, generate_random_initial_state
from creation_of_test_data.simulate_ode import simulate_ode, write_settings_into_file, write_data_file
import numpy as np
import sys

"""
This is a command line tool to generate timeseries data from a given boolnet file.
The idea is to convert bnet file using odefy into an ODE-system.
The ODE-system is then uniformly parametrized and used to generate time series data.
"""

if __name__ == "__main__":
    if len(sys.argv) != 8:
        print("Wrong input.")
        print("1. Argument: name of bnet file")
        print("2. Argument: Name of output file")
        print("3. Argument: [t1, t2] time interval chosen for simulation")
        print("4. Argument: number of sample points")
        print("5. Argument:: [k1,k2] range from which hill exponents are choosen uniformly")
        print("6. Argument:: [theta1,theta2] range from which thresholds are choosen uniformly")
        print("7. Argument:: [lifetime1,lifetime2] range from which lifetimes are choosen uniformly")
        print("Example: python3 create_continuous_data.py bnet.txt data.txt [0,10] 10 [1,5] [0.3,0.7]")
        sys.exit()
    name_of_bnet_file = sys.argv[1]
    name_of_output_file1 = sys.argv[2]+'.csv'
    name_of_output_file = name_of_output_file1.replace('.bnet','')
    time_interval = list(map(float, sys.argv[3][1:-1].split(","))) # Convert string "[a,b]" into list of numbers [a,b]
    number_sample_points = sys.argv[4]
    hill_exponents_range = list(map(float, sys.argv[5][1:-1].split(",")))
    hill_tresholds_range = list(map(float, sys.argv[6][1:-1].split(",")))
    lifetime_range = list(map(float, sys.argv[7][1:-1].split(",")))
    with open(name_of_bnet_file, 'r') as myfile:
        bnet_string = myfile.read()

    # Get random parameters and an initial value
    parameters_to_choose = get_random_parameters(range_lifetime=lifetime_range,
                                                 range_threshold=hill_tresholds_range,
                                                 range_hillcoefficient=hill_exponents_range, bnet=bnet_string)
    initial_state = generate_random_initial_state(parameters_to_choose)
    t_values = np.linspace(time_interval[0], time_interval[1], number_sample_points)

    # Simulate the ODE and write the result and parameters used for the simulation to a file
    concentrations, list_to_dict, dict_to_list, result_of_interpolation = simulate_ode(bnet_string, parameters_to_choose,
                                                                                       initial_state, t_values)
    write_data_file(name_of_output_file, list_to_dict, t_values,
                    concentrations)
    write_settings_into_file(
        name_of_output_file+"_parameters",
        list_to_dict, dict_to_list, result_of_interpolation,
        t_values, parameters_to_choose, initial_state)

    print("Simulation succeeded. The chosen parameters for the simulation can be found in the file "+name_of_output_file+"_parameters.")