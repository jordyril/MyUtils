# =============================================================================
# PACKAGES
# =============================================================================
import numpy as np
import numpy.linalg as la
import scipy.linalg as sla
# =============================================================================
# FUNCTIONS
# =============================================================================


def returns(mu, sigma, num_time_points, num_sims):
    """
    generate num_sims of
    r_i \sim N(\mu, \sigma^2)
    """
    # generate standard normal variables
    returns = np.random.normal(0, 1, (num_sims, num_time_points))

    # transform the standard normal to variables with a variance of $\sigma^2
    returns *= sigma

    # add a drift
    returns += mu

    return returns
