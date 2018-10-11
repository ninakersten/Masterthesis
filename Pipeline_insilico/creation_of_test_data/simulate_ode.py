from scipy.integrate import ode
import matplotlib.pyplot as plt
from creation_of_test_data.odefy_in_python.odefy_in_python import multivariate_polynomial_interpolation, get_template_for_parameters_of_ODE_system, get_corresponding_ODE_system
import scipy.integrate
import numpy as np
import os.path


#from creation_of_test_data.examples.bnet_mini_example import bnet
#from creation_of_test_data.examples.bnet_mini_examples_odefy_parameters import parameters, initial_state

#from creation_of_test_data.examples.bnet_talk_example import bnet
#from creation_of_test_data.examples.bnet_talk_example_odefy_parameters import parameters, initial_state

stoppingTime = 10.0
number_of_steps = 10**2 # Anzahl der Iterationen
dt = stoppingTime/number_of_steps # Schrittgröße


def get_interpolation(bnet):
    """
    Returns from a bnet string the interpolated polynomial
    :param bnet: bnet string
    :param initial_state:
    :return: a multivariate polynomial representing the result of the interpolation,
    a numbering of the components of the network represented as a dictionary, the inverse mapping,
     i.e. the number each component obtained
    """
    result_of_interpolation = multivariate_polynomial_interpolation(bnet)
    parameters_to_choose = get_template_for_parameters_of_ODE_system(result_of_interpolation)
    # create a mapping of the form {1,...,number of components} -> {names of componentes}
    list_to_dict = {number: key for (number, key) in zip(range(len(result_of_interpolation.dictionary_of_polynomials.keys())), result_of_interpolation.dictionary_of_polynomials.keys())}
    # create the inverse mapping, i.e. of the form {names of componentes}-> {1,...,number of components}
    dict_to_list = {list_to_dict[key]: key for key in list_to_dict.keys()}
    return result_of_interpolation, list_to_dict, dict_to_list

def produce_ODE_system(result_of_interpolation, parameters, state_in_list_form_to_dictionary, state_in_dictionary_form_to_list):
    """
    Takes the result of a multivariate polynomial interpolation and
    the corresponding parameters and returns the rhs of an ODE-system.
    :param result_of_interpolation: multivariate polynomial
    :param parameters: set of paramters
    :return: rhs of ODE-system
    """
    ODE_system = get_corresponding_ODE_system(result_of_interpolation, parameters)
    def f(x, t):
        x_dict = state_in_list_form_to_dictionary(x)
        return state_in_dictionary_form_to_list(ODE_system(x_dict))
    return f

#ToDo: Remove
def simulate(name_of_setting_file, name_of_data_file, result_of_interpolation, parameters, initial_state):
    """
    Takes the result of an interpolation and simulates the corresponding ODE-system
    :param name_of_setting_file:
    :param name_of_data_file:
    :param result_of_interpolation:
    :param parameters:
    :param initial_state:
    :param fixed_components:
    :return:
    """
    #f = produce_ODE_system(result_of_interpolation, parameters)

    f = produce_ODE_system(result_of_interpolation, parameters)

    # Solving the ODE-system
    x0 = state_in_dictionary_form_to_list(initial_state)
    y = ode(f).set_integrator('lsoda')
    y.set_initial_value(x0, 0.0) # set initial value at time = 0
    evaluationTimes = [0.0] # initialized
    solution = [[y.t]+ x0] # save the first time step
    print(solution)
    while y.successful() and y.t < stoppingTime:
        evaluationTimes += [y.t+dt]
        y.integrate(y.t+dt)
        # print(str(y.t+dt))
        solution += [[y.t]+ list(y.y)]

    if y.successful() is False:
        print("Something went wrong during r.integrate()")

    # Save data
    settings_file = open(name_of_setting_file, 'w')
    settings_file.write("internal numbering of variables: "+str(list_to_dict)+"\n")
    settings_file.write("internal numbering of variables: "+str(dict_to_list)+"\n")
    settings_file.write("initial state: "+str(initial_state)+"\n")
    settings_file.write("stopping time: "+str(stoppingTime)+"\n")
    settings_file.write("number of steps: " + str(number_of_steps)+"\n")
    settings_file.write("stepsize: "+str(dt)+"\n")
    settings_file.write("parameters of ODE_system: "+str(parameters)+"\n")
    settings_file.write("result_of_interpolation: " + str(result_of_interpolation.dictionary_of_polynomials) + "\n")
    settings_file.close()

    data_file = open(name_of_data_file, 'w')
    data_file.write(",,,Slide ID,"+",".join( [list_to_dict[i] for i in range(len(list_to_dict.keys()))] )+"\n")
    data_file.write(",,,Antibody Name,"+",".join( [list_to_dict[i] for i in range(len(list_to_dict.keys()))] )+"\n")
    data_file.write(",,,HUGO ID,"+",".join( [list_to_dict[i] for i in range(len(list_to_dict.keys()))] )+"\n")
    data_file.write("Cell Line,Inhibitor,Stimulus,Timepoint\n")
    data_file.write("\n".join("C1,no,Insulin,"+",".join([str(el) for el in x]) for x in solution))
    data_file.close()

    # Plot solution

    plt.ion()
    plt.axis([0.0, stoppingTime, 0.0, 1.1])
    for i in range(len(x0)):
        componentOfSolution = [solution[j][i+1] for j in range(len(solution))] # extract i-th component of solution vector
        plt.plot(evaluationTimes, componentOfSolution, label=list_to_dict[i])

    plt.ylabel('Concentrations of components in the network')
    plt.xlabel('Time')
    plt.legend(loc=0)
    plt.title("Trajectory of the solutions of the ODE-system")
    plt.show(block=True)

#-------------------------------------------------------------------------------------
def simulate_ode(bnet, parameters, initial_state, timepoints):
    result_of_interpolation, list_to_dict, dict_to_list = get_interpolation(bnet)

    def state_in_dictionary_form_to_list(state):
        return [state[list_to_dict[i]] for i in range(len(state.keys()))]

    def state_in_list_form_to_dictionary(state):
        return {list_to_dict[index]: state[index] for index in list_to_dict.keys()}

    f = produce_ODE_system(result_of_interpolation, parameters, state_in_list_form_to_dictionary, state_in_dictionary_form_to_list)
    x0 = state_in_dictionary_form_to_list(initial_state)
    result = scipy.integrate.odeint(f, x0, timepoints)
    return result, list_to_dict, dict_to_list, result_of_interpolation

def write_settings_into_file(name_of_setting_file, list_to_dict, dict_to_list, result_of_interpolation, t_values, parameters, initial_state):
    save_path = './PyBoolNet/CSV_insilico/'
    name_of_setting_file1 = name_of_setting_file.replace('./PyBoolNet/bnet_data_insilico/','')
    completeName = os.path.join(save_path, name_of_setting_file1)
    settings_file = open(completeName, 'w')
    settings_file.write("internal numbering of variables: "+str(list_to_dict)+"\n")
    settings_file.write("internal numbering of variables: "+str(dict_to_list)+"\n")
    settings_file.write("initial state: "+str(initial_state)+"\n")
    settings_file.write("\n")
    settings_file.write("\n")
    settings_file.write("\n")
    settings_file.write("parameters of ODE_system: "+str(parameters)+"\n")
    settings_file.write("result_of_interpolation: " + str(result_of_interpolation.dictionary_of_polynomials) + "\n")
    settings_file.close()

 

def write_data_file(name_of_data_file, list_to_dict, t_values, concentrations):
    solution = [[t] + list(x) for t, x in zip(t_values, concentrations)]
    save_path = './PyBoolNet/CSV_insilico/'
    name_of_data_file1 = name_of_data_file.replace('./PyBoolNet/bnet_data_insilico/','')
    completeName1 = os.path.join(save_path, name_of_data_file1)
    data_file = open(completeName1, 'w')
    data_file.write(",,,Slide ID,"+",".join( [list_to_dict[i] for i in range(len(list_to_dict.keys()))] )+"\n")
    data_file.write(",,,Antibody Name,"+",".join( [list_to_dict[i] for i in range(len(list_to_dict.keys()))] )+"\n")
    data_file.write(",,,HUGO ID,"+",".join( [list_to_dict[i] for i in range(len(list_to_dict.keys()))] )+"\n")
    data_file.write("Cell Line,Inhibitor,Stimulus,Timepoint\n")
    data_file.write("\n".join("C1,no,Insulin,"+",".join([str(el) for el in x]) for x in solution))
    data_file.close()



if __name__ == "__main__":
    t_values = np.linspace(0,4,10)
    concentrations, list_to_dict, dict_to_list, result_of_interpolation = simulate_ode(bnet, parameters, initial_state, t_values)
    print(t_values)
    print(concentrations)
    write_settings_into_file("settings_of_simulation", list_to_dict, dict_to_list, result_of_interpolation, t_values)
    write_data_file("data_of_simulation", list_to_dict, t_values, concentrations)

    plt.plot(t_values, concentrations)
    plt.show()

"""
interpolation_result_filename = "interpolation_result"
interpolation_result_file = open(interpolation_result_filename, 'w')
for key in result_of_interpolation.dictionary_of_polynomials.keys():
    interpolation_result_file.write(str(key)+", "+str(result_of_interpolation.dictionary_of_polynomials[key])+"\n")
interpolation_result_file.close()

simulate(name_of_setting_file="settings_reference", name_of_data_file="data_reference",
         result_of_interpolation=result_of_interpolation, parameters=parameters, initial_state=initial_state)
"""