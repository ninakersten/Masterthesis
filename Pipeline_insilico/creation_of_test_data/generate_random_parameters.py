from creation_of_test_data.odefy_in_python.odefy_in_python import multivariate_polynomial_interpolation, get_template_for_parameters_of_ODE_system
from random import uniform

def generate_random_initial_state(parameters_to_choose):
    initial_state = {}
    for key in parameters_to_choose.keys():
        if not key.startswith("d_"):
            initial_state[key] = uniform(0,1)
    return initial_state

def get_random_parameters(range_lifetime, range_threshold, range_hillcoefficient, bnet):
    """
    For a given bnet-file it returns all parameters necessary to define an ODE-system generated with odefy.
    The parameters are randomly chosen.
    :param range_lifetime:
    :param range_threshold:
    :param range_hillcoefficient:
    :param bnet:
    :return: parameters
    """
    result_of_interpolation = multivariate_polynomial_interpolation(bnet)
    parameters_to_choose = get_template_for_parameters_of_ODE_system(result_of_interpolation)
    for key in parameters_to_choose.keys():
        if key.startswith("d_"):
            parameters_to_choose[key] = uniform(*range_lifetime)
        else:
            for second_key in parameters_to_choose[key].keys():
                parameters_to_choose[key][second_key] = (uniform(*range_threshold), uniform(*range_hillcoefficient))
    return parameters_to_choose

def generate_experimental_setup(range_lifetime, range_threshold, range_hillcoefficient, number_of_initial_states, bnets):
    experiments = {}
    for bnet, i in zip(bnets, range(len(bnets))):
        experiments["experiment_"+str(i)] = {"bnet": bnet}
        parameters = get_random_parameters(range_lifetime, range_threshold, range_hillcoefficient, bnet)
        experiments["experiment_" + str(i)]["parameters"] = parameters
        experiments["experiment_" + str(i)]["initial_states"] = [generate_random_initial_state(parameters) for i in range(number_of_initial_states)]

    return experiments
