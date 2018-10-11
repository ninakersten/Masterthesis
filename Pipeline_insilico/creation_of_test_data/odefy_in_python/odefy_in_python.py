from PyBoolNet import FileExchange
from PyBoolNet.StateTransitionGraphs import successor_synchronous, state2str
import itertools
from sympy import *


def create_function(bnet):
    """
    Converts the bnet string into a python function
    :param bnet:
    :return: python function representing the Boolean function encoded in the bnet string
    """
    def func(state):
        return successor_synchronous(func.primes, state)
    func.primes = FileExchange.bnet2primes(bnet)
    return func

def get_relevant_input_variables(boolean_func, component):
    """
    For a Boolean function boolean_func[component] the components it depends on are returned
    :param boolean_func: Boolean function
    :param component: which component from the network is meant
    :return: all components the function depends on
    """
    input_variables = []
    null_implicants = boolean_func.primes[component][0]
    for implicant in null_implicants:
        input_variables += implicant.keys()
    return list(set(input_variables))

def get_table_of_ones_for_component(boolean_func, component):
    """
    Collect all states where the Boolean function boolean_func[component] evaluates to one
    :param boolean_func: Boolean function
    :param component: The component we are interested in
    :return: all states (of the components the functions depends on) which lead to an evaluation of one.
    """
    list_of_variables = get_relevant_input_variables(boolean_func, component)
    input_length = len(list_of_variables)
    complete_state = {key: 0 for key in boolean_func.primes.keys()}
    table_of_ones = []
    for element in itertools.product((0,1), repeat=input_length):
        state = {list_of_variables[i]: element[i] for i in range(input_length)}
        for key in state.keys():
            complete_state[key] = state[key]
        succ = boolean_func(state2str(complete_state))[component]
        if succ:
            table_of_ones += [state]
    return table_of_ones

def assemble_component_polynomial_from_truth_table(table_of_ones, names_pyBoolNet_to_sympy, variable_names_sympy):
    """
    We use entries where the function evaluates to one to construct a multivariate polynomial.
    :param table_of_ones: all states where the polynomial should evaluate to one
    :param names_pyBoolNet_to_sympy:
    :param variable_names_sympy:
    :return: Returns a polynomial representing the multivariate interpolation
    """
    # For each component in the network we need to interpolate a polynomial
    # Therefore, we iterate over  all the variables in variable_names_pyBoolNet
    multivariate_interpolation = 0
    for truth_value in table_of_ones:
        monomial = 1
        for key in truth_value.keys():
            if truth_value[key]:
                monomial *= names_pyBoolNet_to_sympy[key]
            else:
                monomial *= (1 - names_pyBoolNet_to_sympy[key])
        multivariate_interpolation += monomial
    return Poly(multivariate_interpolation, *variable_names_sympy,
                                                    domain='RR')

def assemble_polynomial(boolean_func):
    """
    Computes the polynomial interpolation of a Boolean function
    :param boolean_func: Boolean function
    :return: For each component the multivariate polynomial interpolation is returned
    """
    variable_names_pyBoolNet = list(boolean_func.primes.keys())
    variable_names_sympy = symbols(",".join(list(variable_names_pyBoolNet)))
    names_pyBoolNet_to_sympy = {var1: var2 for var1, var2 in zip(variable_names_pyBoolNet, variable_names_sympy)}


    dictionary_of_polynomials = {var_pyBoolNet: None for var_pyBoolNet in variable_names_pyBoolNet}
    for variable_name in variable_names_pyBoolNet:
        table_of_ones = get_table_of_ones_for_component(boolean_func, variable_name)
        polynomial = assemble_component_polynomial_from_truth_table(table_of_ones, names_pyBoolNet_to_sympy, variable_names_sympy)
        dictionary_of_polynomials[variable_name] = polynomial
    return dictionary_of_polynomials, names_pyBoolNet_to_sympy

def multivariate_polynomial_interpolation(bnet_string):
    """
    Converts a bnet_string into its multivariate polynomial interpolation
    :param bnet_string:
    :return: a function with function.variable_names_pyBoolNet, function..dictionary_of_polynomials, function.names_pyBoolNet_to_sympy
    """
    func = create_function(bnet_string)
    #table_of_ones = get_table_of_ones(func)
    variable_names_pyBoolNet = list(func.primes.keys())
    dictionary_of_polynomials, names_pyBoolNet_to_sympy = assemble_polynomial(func)
    #dictionary_of_polynomials, names_pyBoolNet_to_sympy = assemble_polynomial_from_truth_table(table_of_ones)
    def result_of_interpolation(state):
        state = {func_var: {names_pyBoolNet_to_sympy[var_pyBoolNet]: state[func_var][var_pyBoolNet] for var_pyBoolNet in state[func_var].keys()}
                 for func_var in state.keys()}
        result = {var_pyBoolNet: (dictionary_of_polynomials[var_pyBoolNet].eval(state[var_pyBoolNet])).LC()
                  for var_pyBoolNet in variable_names_pyBoolNet}
        return result

    result_of_interpolation.variable_names_pyBoolNet = variable_names_pyBoolNet
    result_of_interpolation.dictionary_of_polynomials = dictionary_of_polynomials
    result_of_interpolation.names_pyBoolNet_to_sympy = names_pyBoolNet_to_sympy
    return result_of_interpolation

def get_variables_of_polynomial(polynomial, names_pyBoolNet_to_sympy):
    depends_on = []
    for key in names_pyBoolNet_to_sympy.keys():
        if degree(polynomial, gen=names_pyBoolNet_to_sympy[key]) > 0:
            depends_on += [key]
    return depends_on

def get_template_for_parameters_of_ODE_system(result_of_interpolation):
    """
    Returns the parameters in the form "coefficient", "threshold" and a d value
    :param result_of_interpolation:
    :return: template for paramters
    """
    parameters = {key: None for key in result_of_interpolation.dictionary_of_polynomials.keys()}
    for key in result_of_interpolation.dictionary_of_polynomials.keys():
        variables_of_polynomial = get_variables_of_polynomial(result_of_interpolation.dictionary_of_polynomials[key],
                                    result_of_interpolation.names_pyBoolNet_to_sympy)
        parameters[key] = {var:("coefficient", "threshold") for var in variables_of_polynomial}
        parameters['d_'+key] = "life-time"
    return parameters

def hill_function(x, threshold, coefficient):
    return pow(x, coefficient)/(pow(x, coefficient)+pow(threshold, coefficient))

def get_corresponding_ODE_system(result_of_interpolation, parameters):
    """
    Construct the rhs of an ODE-system based on the interpolation of the Boolean function and the specified paramters.
    :param result_of_interpolation:
    :param parameters:
    :return: right hand side of the ODE-system
    """
    variable_names_pyBoolNet = result_of_interpolation.variable_names_pyBoolNet
    def ODE_system(state):
        variable_names_pyBoolNet = ODE_system.variable_names_pyBoolNet
        parameters = ODE_system.parameters
        result_of_interpolation = ODE_system.result_of_interpolation
        hill_functions_of_state = {}
        for component_to_compute in variable_names_pyBoolNet:
            hill_functions_of_state[component_to_compute] = {}
            for var_in_this_function in parameters[component_to_compute].keys():
                coefficient, threshold = parameters[component_to_compute][var_in_this_function]
                hill_functions_of_state[component_to_compute][var_in_this_function] = hill_function(state[var_in_this_function], threshold, coefficient)
        result_of_interpolation_evaluation = result_of_interpolation(hill_functions_of_state)
        result = {var: parameters["d_"+var]*(result_of_interpolation_evaluation[var]-state[var])  for var in result_of_interpolation_evaluation}
        return result

    ODE_system.variable_names_pyBoolNet = variable_names_pyBoolNet
    ODE_system.parameters = parameters
    ODE_system.result_of_interpolation = result_of_interpolation
    return ODE_system


#result_of_interpolation = multivariate_polynomial_interpolation(bnet)
#parameters = get_parameters_of_ODE_system(result_of_interpolation)
#parameters = {'x2': {'x3': (2, 0.5), 'x1': (2, 0.5)}, 'x3': {'x1': (2, 0.5)}, 'x1': {'x2': (2, 0.5)}, 'd_x1': 1, 'd_x2': 2, 'd_x3': 3}
#ODE_system = get_corresponding_ODE_system(result_of_interpolation, parameters)
#state = {'x1':0.1, 'x2':0.3, 'x3':0.2}
#print(result_of_interpolation())
#print(ODE_system(state))



#state = "110"
#print(func(state))
