# =============================================================================
# Packages
# =============================================================================
import numpy as np

# =============================================================================
# FUNCTIONS
# =============================================================================


def check_within_ci(parameter, ci, printing=True):
    """
    Checks if a parameter is within a given confidence interval
    """
    x = True if ci[0] <= parameter <= ci[1] else False
    if printing:
        print('WITHIN the CI' if x else 'OUTSIDE the CI')

    return x


def comparison_actual_solution(estimation, actual_values, limit=10e-6):
    dash = '-' * 40
    distance = actual_values - estimation
    print('Comparison with actual solution')
    print(dash)
    print('{:<55s}'.format("Distance from actual values (act - est):"),
          distance)
    if not np.all(abs(distance) <= limit):
        print(55 * ' ', '=> Something is WRONG')
    return None


def variance_Delta_method(Jacobian, Sigma):
    """
    Given the Jacobian (matrix) and the Var-Cov (matrix), returns the variance
    using the delta-method
    """
    var = Jacobian @ Sigma @ Jacobian
    return var


def MSE(estimated_param, actual_param):
    """
    Mean Squared Error
    """
    return np.mean((estimated_param - actual_param)**2, axis=0)


def MPE(estimated_param, actual_param):
    """
    Mean Percentage Error
    """
    return np.mean((actual_param - estimated_param) / actual_param, axis=0)


def MAPE(estimated_param, actual_param):
    """
    Mean Absolute Percentage Error
    """
    return np.mean(np.abs((actual_param - estimated_param) / actual_param), axis=0)
